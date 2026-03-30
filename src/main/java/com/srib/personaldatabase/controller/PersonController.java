package com.srib.personaldatabase.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.service.PersonService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/persons")
@RequiredArgsConstructor
@Tag(name = "Person API", description = "API for å håndtere personer")
public class PersonController {
    private final PersonService personService;

    @Operation(summary = "Hent personer", description = "Returnerer en liste med personer. Filtrer med ?role=rolle eller søk med ?search=navn")
    @GetMapping
    public List<Person> getPersons(
            @RequestParam(required = false) String role,
            @RequestParam(required = false) String search) {
        if (search != null && !search.isBlank()) {
            return personService.searchPersonsByName(search);
        }
        if (role != null && !role.isBlank()) {
            return personService.getPersonsByRole(role);
        }
        return personService.getAllPersons();
    }

    @Operation(summary = "Legge til en person", description = "Legger til en person")
    @PostMapping
    public Person createPerson(@RequestBody Person person) {
        return personService.createPerson(person);
    }

    @Operation(summary = "Oppdater en person", description = "Oppdaterer en eksisterende person via ID")
    @PutMapping("/{id}")
    public Person updatePerson(@PathVariable Long id, @RequestBody Person person) {
        return personService.updatePerson(id, person);
    }

    @Operation(summary = "Slett en person", description = "Sletter en person via ID")
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deletePerson(@PathVariable Long id) {
        personService.deletePerson(id);
        return ResponseEntity.noContent().build();
    }

    @Operation(summary = "Sett signert medarbeideravtale", description = "Registrerer dato for signert medarbeideravtale")
    @PutMapping("/{id}/contract")
    public Person setSignedContract(@PathVariable Long id, @RequestBody Map<String, String> body) {
        return personService.setSignedContract(id, body.get("contractDate"));
    }

    @Operation(summary = "Fjern signert medarbeideravtale", description = "Fjerner registrert dato for signert medarbeideravtale")
    @DeleteMapping("/{id}/contract")
    public Person removeSignedContract(@PathVariable Long id) {
        return personService.removeSignedContract(id);
    }

    @Operation(summary = "Fjern person fra kurs", description = "Fjerner en person fra et kurs via ID")
    @DeleteMapping("/{personId}/courses/{courseId}")
    public ResponseEntity<Void> removePersonFromCourse(@PathVariable Long personId, @PathVariable Long courseId) {
        personService.removePersonFromCourse(personId, courseId);
        return ResponseEntity.noContent().build();
    }
}
