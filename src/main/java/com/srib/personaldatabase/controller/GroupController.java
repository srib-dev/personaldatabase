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

import com.srib.personaldatabase.domain.Group;
import com.srib.personaldatabase.service.GroupService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/groups")
@RequiredArgsConstructor
@Tag(name = "Group API", description = "API for å håndtere grupper og medlemskap")
public class GroupController {

    private final GroupService groupService;

    @Operation(summary = "Hent alle grupper", description = "Returnerer en liste med alle grupper")
    @GetMapping
    public List<Group> getGroups() {
        return groupService.getAllGroups();
    }

    @Operation(summary = "Lag en ny gruppe", description = "Legger til en ny gruppe")
    @PostMapping
    public Group createGroup(@RequestBody Group group) {
        return groupService.createGroup(group);
    }

    @Operation(summary = "Oppdater en gruppe", description = "Oppdaterer en eksisterende gruppe via ID")
    @PutMapping("/{id}")
    public Group updateGroup(@PathVariable Long id, @RequestBody Group group) {
        return groupService.updateGroup(id, group);
    }

    @Operation(summary = "Slett en gruppe", description = "Sletter en gruppe via ID")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteGroup(@PathVariable Long id) {
        groupService.deleteGroup(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Legg en person til i en gruppe", description = "Knytter en eksisterende person til en gruppe via ID")
    @PostMapping("/{groupId}/persons/{personId}")
    public ResponseEntity<Void> addPersonToGroup(@PathVariable Long groupId, @PathVariable Long personId) {
        groupService.addPersonToGroup(groupId, personId);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Fjern en person fra en gruppe", description = "Fjerner en person fra en gruppe via ID")
    @DeleteMapping("/{groupId}/persons/{personId}")
    public ResponseEntity<Void> removePersonFromGroup(@PathVariable Long groupId, @PathVariable Long personId) {
        groupService.removePersonFromGroup(groupId, personId);
        return ResponseEntity.noContent().build();
    }
}
