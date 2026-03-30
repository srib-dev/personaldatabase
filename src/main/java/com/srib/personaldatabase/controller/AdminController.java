package com.srib.personaldatabase.controller;

import java.util.List;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.srib.personaldatabase.domain.Admin;
import com.srib.personaldatabase.service.AuthService;

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

    @Operation(summary = "Hent alle admin-brukere")
    @GetMapping("/admins")
    public List<Admin> getAllAdmins() {
        return authService.getAllAdmins();
    }

    @Operation(summary = "Oppdater en admin-bruker")
    @PutMapping("/admins/{id}")
    public ResponseEntity<RegisterAdminResponse> updateAdmin(@PathVariable Long id, @RequestBody UpdateAdminRequest request) {
        Admin admin = authService.updateAdmin(id, request.username(), request.password());
        return ResponseEntity.ok(new RegisterAdminResponse(admin.getId(), admin.getUsername()));
    }

    @Operation(summary = "Slett en admin-bruker")
    @DeleteMapping("/admins/{id}")
    public ResponseEntity<Void> deleteAdmin(@PathVariable Long id) {
        authService.deleteAdmin(id);
        return ResponseEntity.noContent().build();
    }

    public record RegisterAdminRequest(String username, String password) {}
    public record RegisterAdminResponse(Long id, String username) {}

    public record LoginRequest(String username, String password) {}
    public record LoginResponse(boolean succes, String message) {}

    public record UpdateAdminRequest(String username, String password) {}
}
