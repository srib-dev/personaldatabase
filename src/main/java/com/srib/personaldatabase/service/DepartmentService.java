package com.srib.personaldatabase.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.srib.personaldatabase.domain.Department;
import com.srib.personaldatabase.domain.Group;
import com.srib.personaldatabase.repository.DepartmentRepository;
import com.srib.personaldatabase.repository.GroupRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class DepartmentService {

    private final DepartmentRepository departmentRepository;
    private final GroupRepository groupRepository;

    public List<Department> getAllDepartments() {
        return departmentRepository.findAll();
    }

    public Department getDepartment(Long id) {
        return departmentRepository.findById(id).orElseThrow();
    }

    public Department createDepartment(Department department) {
        return departmentRepository.save(department);
    }

    public Department updateDepartment(Long id, Department updated) {
        Department existing = departmentRepository.findById(id).orElseThrow();
        existing.setDepartment_name(updated.getDepartment_name());
        existing.setDepartment_description(updated.getDepartment_description());
        return departmentRepository.save(existing);
    }

    public void deleteDepartment(Long id) {
        Department department = departmentRepository.findById(id).orElseThrow();
        for (Group group : department.getGroups()) {
            group.setDepartment(null);
            groupRepository.save(group);
        }
        departmentRepository.delete(department);
    }

    public void addGroupToDepartment(Long departmentId, Long groupId) {
        Department department = departmentRepository.findById(departmentId).orElseThrow();
        Group group = groupRepository.findById(groupId).orElseThrow();
        group.setDepartment(department);
        groupRepository.save(group);
    }

    public void removeGroupFromDepartment(Long departmentId, Long groupId) {
        Group group = groupRepository.findById(groupId).orElseThrow();
        if (group.getDepartment() != null && group.getDepartment().getDepartment_id().equals(departmentId)) {
            group.setDepartment(null);
            groupRepository.save(group);
        }
    }
}
