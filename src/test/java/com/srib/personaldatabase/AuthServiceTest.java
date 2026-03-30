package com.srib.personaldatabase;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import com.srib.personaldatabase.domain.Admin;
import com.srib.personaldatabase.repository.AdminRepository;
import com.srib.personaldatabase.service.AuthService;

@ExtendWith(MockitoExtension.class)
public class AuthServiceTest {

    @Mock
    private AdminRepository adminRepository;

    @InjectMocks
    private AuthService authService;

    private final BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

    private Admin admin;

    @BeforeEach
    void setUp() {
        admin = new Admin(1L, "admin", encoder.encode("secret"));
    }

    @Test
    @DisplayName("Should register a new admin")
    void registerAdmin() {
        when(adminRepository.findByUsername("newAdmin")).thenReturn(Optional.empty());
        when(adminRepository.save(any(Admin.class))).thenAnswer(inv -> inv.getArgument(0));

        Admin result = authService.registerAdmin("newAdmin", "password");

        assertNotNull(result);
        assertEquals("newAdmin", result.getUsername());
        assertTrue(encoder.matches("password", result.getPasswordHash()));
        verify(adminRepository, times(1)).save(any(Admin.class));
    }

    @Test
    @DisplayName("Should throw when registering a duplicate username")
    void registerAdminDuplicateUsername() {
        when(adminRepository.findByUsername("admin")).thenReturn(Optional.of(admin));

        assertThrows(IllegalArgumentException.class, () -> authService.registerAdmin("admin", "password"));
        verify(adminRepository, never()).save(any());
    }

    @Test
    @DisplayName("Should authenticate with correct password")
    void authenticateSuccess() {
        when(adminRepository.findByUsername("admin")).thenReturn(Optional.of(admin));

        boolean result = authService.authenticate("admin", "secret");

        assertTrue(result);
    }

    @Test
    @DisplayName("Should reject authentication with wrong password")
    void authenticateWrongPassword() {
        when(adminRepository.findByUsername("admin")).thenReturn(Optional.of(admin));

        boolean result = authService.authenticate("admin", "wrong");

        assertFalse(result);
    }

    @Test
    @DisplayName("Should return false when admin not found during authentication")
    void authenticateUnknownUser() {
        when(adminRepository.findByUsername("nobody")).thenReturn(Optional.empty());

        boolean result = authService.authenticate("nobody", "anything");

        assertFalse(result);
    }

    @Test
    @DisplayName("Should find admin by username")
    void findByUsername() {
        when(adminRepository.findByUsername("admin")).thenReturn(Optional.of(admin));

        Optional<Admin> result = authService.findByUsername("admin");

        assertTrue(result.isPresent());
        assertEquals("admin", result.get().getUsername());
    }

    @Test
    @DisplayName("Should return all admins")
    void getAllAdmins() {
        when(adminRepository.findAll()).thenReturn(List.of(admin));

        List<Admin> result = authService.getAllAdmins();

        assertEquals(1, result.size());
        verify(adminRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Should update admin username and password")
    void updateAdmin() {
        when(adminRepository.findById(1L)).thenReturn(Optional.of(admin));
        when(adminRepository.save(any(Admin.class))).thenAnswer(inv -> inv.getArgument(0));

        Admin result = authService.updateAdmin(1L, "updatedAdmin", "newPassword");

        assertEquals("updatedAdmin", result.getUsername());
        assertTrue(encoder.matches("newPassword", result.getPasswordHash()));
        verify(adminRepository, times(1)).save(admin);
    }

    @Test
    @DisplayName("Should delete admin by id")
    void deleteAdmin() {
        doNothing().when(adminRepository).deleteById(1L);

        authService.deleteAdmin(1L);

        verify(adminRepository, times(1)).deleteById(1L);
    }
}
