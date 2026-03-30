package com.srib.personaldatabase.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.srib.personaldatabase.domain.Course;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.CourseRepository;
import com.srib.personaldatabase.repository.PersonRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PersonService {
    private final PersonRepository personRepository;
    private final CourseRepository courseRepository;

    public List<Person> getAllPersons() {
        return personRepository.findAll();
    }

    public Person createPerson(Person person) {
        return personRepository.save(person);
    }

    public List<Person> getPersonsByRole(String roleName) {
        return personRepository.findByRole(roleName);
    }

    public List<Person> searchPersonsByName(String name) {
        return personRepository.findByFirstNameContainingIgnoreCaseOrLastNameContainingIgnoreCase(name, name);
    }

    public Person updatePerson(Long id, Person updated) {
        Person existing = personRepository.findById(id).orElseThrow();
        existing.setFirstName(updated.getFirstName());
        existing.setLastName(updated.getLastName());
        existing.setStreetName(updated.getStreetName());
        existing.setPostBox(updated.getPostBox());
        existing.setPhoneNumber(updated.getPhoneNumber());
        existing.setEmail(updated.getEmail());
        existing.setInstitution(updated.getInstitution());
        existing.setStudentCardNumber(updated.getStudentCardNumber());
        existing.setRole(updated.getRole());
        existing.setLastSignedContract(updated.getLastSignedContract());
        return personRepository.save(existing);
    }

    public void deletePerson(Long id) {
        personRepository.deleteById(id);
    }

    public Person setSignedContract(Long id, String contractDate) {
        Person person = personRepository.findById(id).orElseThrow();
        person.setLastSignedContract(contractDate);
        return personRepository.save(person);
    }

    public Person removeSignedContract(Long id) {
        Person person = personRepository.findById(id).orElseThrow();
        person.setLastSignedContract(null);
        return personRepository.save(person);
    }

    public void removePersonFromCourse(Long personId, Long courseId) {
        Person person = personRepository.findById(personId).orElseThrow();
        Course course = courseRepository.findById(courseId).orElseThrow();
        person.getCourses().remove(course);
        personRepository.save(person);
    }
}
