package com.srib.personaldatabase.controller;

import org.springframework.http.HttpStatus;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.srib.personaldatabase.service.AuthService;

import com.srib.personaldatabase.domain.Admin;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("api/admin/auth")
@RequiredArgsConstructor
@Tag(name = "Admin auth API", description = "Register and login for admin users")
public class AdminController {
    
    private final AuthService authService;

    @Operation(summary = "Register admin")
    @PostMapping("/register")
    public ResponseEntity<RegisterAdminResponse> register(@RequestBody RegisterAdminRequest request) {
        Admin admin = authService.registerAdmin(request.username(), request.password());
        return ResponseEntity.status(HttpStatus.CREATED)
                    .body(new RegisterAdminResponse(admin.getId(), admin.getUsername()));
    }

    @Operation(summary = "Login admin") 
    @PostMapping("/login")
    public ResponseEntity<LoginResponse> login(@RequestBody LoginRequest request) {
        boolean ok = authService.authenticate(request.username(), request.password());
        if (!ok) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(new LoginResponse(false, "Invalid username or password"));
        }
        return ResponseEntity.ok(new LoginResponse(true, "Login succesful"));
    }

    public record RegisterAdminRequest(String username, String password) {}
    public record RegisterAdminResponse(Long id, String username) {}

    public record LoginRequest(String username, String password) {}
    public record LoginResponse(boolean succes, String message) {}

}
