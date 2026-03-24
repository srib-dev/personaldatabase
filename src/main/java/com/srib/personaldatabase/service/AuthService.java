package com.srib.personaldatabase.service;

import org.springframework.stereotype.Service;

import com.srib.personaldatabase.domain.Admin;
import com.srib.personaldatabase.repository.AdminRepository;

import lombok.RequiredArgsConstructor;

import java.util.Optional;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

@Service
@RequiredArgsConstructor
public class AuthService {

    private final AdminRepository adminRepository;
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
    private final JWTService jWTService;

    public Admin registerAdmin(String username, String rawPassword) {
        adminRepository.findByUsername(username).ifPresent(a -> {
            throw new IllegalArgumentException("Username already exists");
        });
        Admin admin = new Admin();
        admin.setUsername(username);
        admin.setPasswordHash(passwordEncoder.encode(rawPassword));
        return adminRepository.save(admin);
    }

    public String authenticate(String username, String rawPassword) {
        // TODO: Change this quick fix to be more logical
        Admin admin = adminRepository.findByUsername(username).orElse(null);
        if ( admin == null ||
                !passwordEncoder.matches(rawPassword, admin.getPasswordHash()) ) {
            return null;
        }
        return jWTService.generateToken(admin);
    }
    
    public Optional<Admin> findByUsername(String username) {
        return adminRepository.findByUsername(username);
    }
}
