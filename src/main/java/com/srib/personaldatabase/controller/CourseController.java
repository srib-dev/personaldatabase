package com.srib.personaldatabase.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.srib.personaldatabase.domain.Course;
import com.srib.personaldatabase.service.CourseService;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/courses")
@RequiredArgsConstructor
@Tag(name = "Course API", description = "API for å håndtere kurs og deltakere")
public class CourseController {

    private final CourseService courseService;

    @Operation(summary = "Hent alle kurs", description = "Returnerer en liste med alle kurs")
    @GetMapping
    public List<Course> getCourses() {
        return courseService.getAllCourses();
    }

    @Operation(summary = "Lag et nytt kurs", description = "Legger til et nytt kurs")
    @PostMapping
    public Course createCourse(@RequestBody Course course) {
        return courseService.createCourse(course);
    }

    @Operation(summary = "Legg en person til i et kurs", description = "Knytter en eksisterende person til et kurs via ID")
    @PostMapping("/{courseId}/persons/{personId}")
    public void addPersonToCourse(@PathVariable Long courseId, @PathVariable Long personId) {
        courseService.addPersonToCourse(courseId, personId);
    }
}