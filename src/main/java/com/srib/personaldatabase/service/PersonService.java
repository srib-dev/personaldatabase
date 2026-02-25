package com.srib.personaldatabase.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.PersonRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;

    public List<Person> getAllPersons() {
        return personRepository.findAll();
    }

    public Person createPerson(Person person) {
        return personRepository.save(person);
    }

    public List<Person> getPersonsByRole(String roleName) {
        return personRepository.findByRole(roleName);
    }
}
