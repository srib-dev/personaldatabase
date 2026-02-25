package com.srib.personaldatabase.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
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

    @Operation(summary = "Hent personer", description = "Returnerer en liste med personer kan legge til filter, for Rolle så er det for eksempel /api/persons?role=rolle")
    @GetMapping
    public List<Person> getPersons(
            //Add RequestParam here with more filters
            @RequestParam(required = false) String role) 
        
        {
        if (role == null || role.isBlank()) {
            return personService.getAllPersons();
        }
        return personService.getPersonsByRole(role);
    }

    @Operation(summary = "Legge til en person", description = "Legger til en person")
    @PostMapping
    public Person createPerson(@RequestBody Person person) {
        return personService.createPerson(person);
    }

    

}
