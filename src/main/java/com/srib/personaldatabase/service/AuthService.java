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

    public Admin registerAdmin(String username, String rawPassword) {
        adminRepository.findByUsername(username).ifPresent(a -> {
            throw new IllegalArgumentException("Username already exists");
        });
        Admin admin = new Admin();
        admin.setUsername(username);
        admin.setPasswordHash(passwordEncoder.encode(rawPassword));
        return adminRepository.save(admin);
    }

    public boolean authenticate(String username, String rawPassword) {
        return adminRepository.findByUsername(username)
            .map(admin -> passwordEncoder.matches(rawPassword, admin.getPasswordHash()))
            .orElse(false);
    }
    
    public Optional<Admin> findByUsername(String username) {
        return adminRepository.findByUsername(username);
    }
}
