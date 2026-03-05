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
public class CourseService {
  private final CourseRepository courseRepository;
  private final PersonRepository personRepository;

  public List<Course> getAllCourses() {
    return courseRepository.findAll();
  }

  public Course createCourse(Course course) {
    return courseRepository.save(course);
  }

  public void addPersonToCourse(Long courseId, Long personId) {
    Person person = personRepository.findById(personId).orElseThrow();
    Course course = courseRepository.findById(courseId).orElseThrow();

    person.getCourses().add(course);
    personRepository.save(person);
  }
}
