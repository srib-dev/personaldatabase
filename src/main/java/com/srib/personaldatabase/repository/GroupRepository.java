package com.srib.personaldatabase.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.srib.personaldatabase.domain.Group;

@Repository
public interface GroupRepository extends JpaRepository<Group, Long> {
}
