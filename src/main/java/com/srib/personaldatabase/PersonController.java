package com.srib.personaldatabase;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/persons")
@RequiredArgsConstructor
@Tag(name = "Person API", description = "API for å håndtere personer")

public class PersonController {
    private final PersonRepository personRepository;

    @Operation(summary = "Hent alle personer", description = "Returnerer en liste med alle personer")
    @GetMapping
    public List<Person> getAllPersons() {
        return personRepository.findAll();
    }
    @Operation(summary = "Legge til en person", description = "Legger til en person")
    @PostMapping
    public Person createPerson(@RequestBody Person person) {
        return personRepository.save(person);
    }

    @Operation(summary = "Hent person utifra rolle", description = "Returnerer en liste med alle personer i rollen")
    @GetMapping("/role/{roleName}")
    public List<Person> getPersonsByRole(@PathVariable String roleName) {
        return personRepository.findByRole(roleName);
    }

}
