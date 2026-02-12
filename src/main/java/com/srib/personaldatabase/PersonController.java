package com.srib.personaldatabase;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;

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




}
