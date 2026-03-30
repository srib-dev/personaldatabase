package com.srib.personaldatabase.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.srib.personaldatabase.domain.Group;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.GroupRepository;
import com.srib.personaldatabase.repository.PersonRepository;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class GroupService {
  private final GroupRepository groupRepository;
  private final PersonRepository personRepository;

  public List<Group> getAllGroups() {
    return groupRepository.findAll();
  }

  public Group createGroup(Group group) {
    return groupRepository.save(group);
  }

  public void addPersonToGroup(Long groupId, Long personId) {
    Person person = personRepository.findById(personId).orElseThrow();
    Group group = groupRepository.findById(groupId).orElseThrow();

    person.getGroups().add(group);
    personRepository.save(person);
  }

  public Group updateGroup(Long id, Group updated) {
    Group existing = groupRepository.findById(id).orElseThrow();
    existing.setGroup_name(updated.getGroup_name());
    existing.setGroup_description(updated.getGroup_description());
    return groupRepository.save(existing);
  }

  public void deleteGroup(Long id) {
    groupRepository.deleteById(id);
  }

  public void removePersonFromGroup(Long groupId, Long personId) {
    Person person = personRepository.findById(personId).orElseThrow();
    Group group = groupRepository.findById(groupId).orElseThrow();
    person.getGroups().remove(group);
    personRepository.save(person);
  }
}
