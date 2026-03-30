package com.srib.personaldatabase;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import com.srib.personaldatabase.domain.Course;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.CourseRepository;
import com.srib.personaldatabase.repository.PersonRepository;
import com.srib.personaldatabase.service.PersonService;

@ExtendWith(MockitoExtension.class)
public class PersonTest {

    @Mock
    private PersonRepository personRepository;

    @Mock
    private CourseRepository courseRepository;

    @InjectMocks
    private PersonService personService;

    private Person p1;
    private Person p2;

    @BeforeEach
    void setUp() {
        p1 = new Person(1L, "Ola", "Nordmann", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
        p2 = new Person(2L, "Kari", "Nordmann", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
    }

    @Test
    @DisplayName("Should return all persons")
    void returnAllPersons() {
        when(personRepository.findAll()).thenReturn(List.of(p1, p2));

        List<Person> result = personService.getAllPersons();

        assertEquals(2, result.size());
        verify(personRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Should create a new person")
    void createPerson() {
        when(personRepository.save(p1)).thenReturn(p1);

        Person result = personService.createPerson(p1);

        assertNotNull(result);
        assertEquals("Ola", result.getFirstName());
        verify(personRepository, times(1)).save(p1);
    }

    @Test
    @DisplayName("Should delete a person by id")
    void deletePerson() {
        doNothing().when(personRepository).deleteById(1L);

        personService.deletePerson(1L);

        verify(personRepository, times(1)).deleteById(1L);
    }

    @Test
    @DisplayName("Should update a person")
    void updatePerson() {
        Person updatedPerson = new Person(1L, "Ole", "Hansen", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
        when(personRepository.findById(1L)).thenReturn(Optional.of(p1));
        when(personRepository.save(any(Person.class))).thenReturn(updatedPerson);

        Person result = personService.updatePerson(1L, updatedPerson);

        assertNotNull(result);
        assertEquals("Ole", result.getFirstName());
        assertEquals("Hansen", result.getLastName());
        verify(personRepository, times(1)).findById(1L);
        verify(personRepository, times(1)).save(any(Person.class));
    }

    @Test
    @DisplayName("Should return persons by role")
    void getPersonsByRole() {
        when(personRepository.findByRole("student")).thenReturn(List.of(p1));

        List<Person> result = personService.getPersonsByRole("student");

        assertEquals(1, result.size());
        verify(personRepository, times(1)).findByRole("student");
    }

    @Test
    @DisplayName("Should search persons by name")
    void searchPersonsByName() {
        when(personRepository.findByFirstNameContainingIgnoreCaseOrLastNameContainingIgnoreCase("ola", "ola"))
                .thenReturn(List.of(p1));

        List<Person> result = personService.searchPersonsByName("ola");

        assertEquals(1, result.size());
        verify(personRepository, times(1))
                .findByFirstNameContainingIgnoreCaseOrLastNameContainingIgnoreCase("ola", "ola");
    }

    @Test
    @DisplayName("Should set signed contract date on a person")
    void setSignedContract() {
        when(personRepository.findById(1L)).thenReturn(Optional.of(p1));
        when(personRepository.save(any(Person.class))).thenReturn(p1);

        Person result = personService.setSignedContract(1L, "2024-01-01");

        assertNotNull(result);
        verify(personRepository, times(1)).findById(1L);
        verify(personRepository, times(1)).save(p1);
    }

    @Test
    @DisplayName("Should remove signed contract from a person")
    void removeSignedContract() {
        p1.setLastSignedContract("2024-01-01");
        when(personRepository.findById(1L)).thenReturn(Optional.of(p1));
        when(personRepository.save(any(Person.class))).thenReturn(p1);

        Person result = personService.removeSignedContract(1L);

        assertNull(result.getLastSignedContract());
        verify(personRepository, times(1)).findById(1L);
        verify(personRepository, times(1)).save(p1);
    }

    @Test
    @DisplayName("Should remove a person from a course")
    void removePersonFromCourse() {
        Course course = new Course(1L, "Math", "Mathematics", new HashSet<>());
        p1.getCourses().add(course);
        when(personRepository.findById(1L)).thenReturn(Optional.of(p1));
        when(courseRepository.findById(1L)).thenReturn(Optional.of(course));
        when(personRepository.save(any(Person.class))).thenReturn(p1);

        personService.removePersonFromCourse(1L, 1L);

        assertFalse(p1.getCourses().contains(course));
        verify(personRepository, times(1)).save(p1);
    }
}
