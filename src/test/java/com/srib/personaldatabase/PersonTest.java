package com.srib.personaldatabase;

import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.*;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.PersonRepository;
import com.srib.personaldatabase.service.PersonService;

@ExtendWith(MockitoExtension.class)
public class PersonTest {

    @Mock
    private PersonRepository personRepository;

    @InjectMocks
    private PersonService personService;

    private Person p1;
    private Person p2;

    @BeforeEach
    void setUp() {
        p1 = new Person(null, "Ola", "Nordmann", null, null, null, null, null, null, null, null, null);
        p2 = new Person(2L, "Kari", "Nordmann", null, null, null, null, null, null, null, null, null);
    }
    @Test
    @DisplayName("Should return all personell")
    void returnAllPersons() {
        when(personRepository.findAll()).thenReturn(List.of(p1,p2));

        List<Person> result = personService.getAllPersons();

        assertEquals(2, result.size());

        verify(personRepository, times(1)).findAll(); 
    }
    @Test
    @DisplayName("Should delete a person by id")
    void deletePerson() {
        doNothing().when(personRepository).deleteById(1L);

        personService.deletePerson(1L);

        verify(personRepository, times(1)).deleteById(1L);
    }

    @Test
    @DisplayName("Should edit a person")
    void updatePerson() {
        Person updatedPerson = new Person(1L, "Ole", "Hansen", null, null, null, null, null, null, null, null, null);
        when(personRepository.findById(1L)).thenReturn(Optional.of(p1));
        when(personRepository.save(any(Person.class))).thenReturn(updatedPerson);

        Person result = personService.updatedPerson(1L, updatedPerson);

        assertNotNull(result);
        assertEquals("Ole", result.getFirstName());
        assertEquals("Hansen", result.getLastName());
        verify(personRepository, times(1)).findById(1L);
        verify(personRepository, times(1)).save(any(Person.class));
    }







}
