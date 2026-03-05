package com.srib.personaldatabase.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.srib.personaldatabase.domain.Course;

@Repository
public interface CourseRepository extends JpaRepository<Course, Long> {
}
