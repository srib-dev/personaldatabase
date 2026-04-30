package com.srib.personaldatabase.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.srib.personaldatabase.domain.Department;

@Repository
public interface DepartmentRepository extends JpaRepository<Department, Long> {
}
