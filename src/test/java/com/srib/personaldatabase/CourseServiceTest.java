package com.srib.personaldatabase;

import java.util.HashSet;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import com.srib.personaldatabase.domain.Course;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.CourseRepository;
import com.srib.personaldatabase.repository.PersonRepository;
import com.srib.personaldatabase.service.CourseService;

@ExtendWith(MockitoExtension.class)
public class CourseServiceTest {

    @Mock
    private CourseRepository courseRepository;

    @Mock
    private PersonRepository personRepository;

    @InjectMocks
    private CourseService courseService;

    private Course c1;
    private Course c2;

    @BeforeEach
    void setUp() {
        c1 = new Course(1L, "INF100", "Introduction to programming", new HashSet<>());
        c2 = new Course(2L, "INF222", "Software architecture", new HashSet<>());
    }

    @Test
    @DisplayName("Should return all courses")
    void getAllCourses() {
        when(courseRepository.findAll()).thenReturn(List.of(c1, c2));

        List<Course> result = courseService.getAllCourses();

        assertEquals(2, result.size());
        verify(courseRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Should create a new course")
    void createCourse() {
        when(courseRepository.save(c1)).thenReturn(c1);

        Course result = courseService.createCourse(c1);

        assertNotNull(result);
        assertEquals("INF100", result.getCourse_name());
        verify(courseRepository, times(1)).save(c1);
    }

    @Test
    @DisplayName("Should add a person to a course")
    void addPersonToCourse() {
        Person person = new Person(1L, "Ola", "Nordmann", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
        when(personRepository.findById(1L)).thenReturn(Optional.of(person));
        when(courseRepository.findById(1L)).thenReturn(Optional.of(c1));
        when(personRepository.save(any(Person.class))).thenReturn(person);

        courseService.addPersonToCourse(1L, 1L);

        assertTrue(person.getCourses().contains(c1));
        verify(personRepository, times(1)).save(person);
    }
}
