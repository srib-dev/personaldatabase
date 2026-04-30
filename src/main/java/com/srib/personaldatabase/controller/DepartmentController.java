package com.srib.personaldatabase.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.srib.personaldatabase.domain.Department;
import com.srib.personaldatabase.service.DepartmentService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/departments")
@RequiredArgsConstructor
@Tag(name = "Department API", description = "API for å håndtere avdelinger og grupper")
public class DepartmentController {

    private final DepartmentService departmentService;

    @Operation(summary = "Hent alle avdelinger")
    @GetMapping
    public List<Department> getDepartments() {
        return departmentService.getAllDepartments();
    }

    @Operation(summary = "Hent en avdeling via ID")
    @GetMapping("/{id}")
    public Department getDepartment(@PathVariable Long id) {
        return departmentService.getDepartment(id);
    }

    @Operation(summary = "Lag en ny avdeling")
    @PostMapping
    public Department createDepartment(@RequestBody Department department) {
        return departmentService.createDepartment(department);
    }

    @Operation(summary = "Oppdater en avdeling via ID")
    @PutMapping("/{id}")
    public Department updateDepartment(@PathVariable Long id, @RequestBody Department department) {
        return departmentService.updateDepartment(id, department);
    }

    @Operation(summary = "Slett en avdeling via ID")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteDepartment(@PathVariable Long id) {
        departmentService.deleteDepartment(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Legg en gruppe til i en avdeling")
    @PostMapping("/{departmentId}/groups/{groupId}")
    public ResponseEntity<Void> addGroupToDepartment(@PathVariable Long departmentId, @PathVariable Long groupId) {
        departmentService.addGroupToDepartment(departmentId, groupId);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Fjern en gruppe fra en avdeling")
    @DeleteMapping("/{departmentId}/groups/{groupId}")
    public ResponseEntity<Void> removeGroupFromDepartment(@PathVariable Long departmentId, @PathVariable Long groupId) {
        departmentService.removeGroupFromDepartment(departmentId, groupId);
        return ResponseEntity.noContent().build();
    }
}
