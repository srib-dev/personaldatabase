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

import com.srib.personaldatabase.domain.Group;
import com.srib.personaldatabase.domain.Person;
import com.srib.personaldatabase.repository.GroupRepository;
import com.srib.personaldatabase.repository.PersonRepository;
import com.srib.personaldatabase.service.GroupService;

@ExtendWith(MockitoExtension.class)
public class GroupTest {

    @Mock
    private GroupRepository groupRepository;

    @Mock
    private PersonRepository personRepository;

    @InjectMocks
    private GroupService groupService;

    private Group g1;
    private Group g2;

    @BeforeEach
    void setUp() {
        g1 = new Group(1L, "Admins", "Admin group", null, new HashSet<>());
        g2 = new Group(2L, "Users", "User group", null, new HashSet<>());
    }

    @Test
    @DisplayName("Should return all groups")
    void getAllGroups() {
        when(groupRepository.findAll()).thenReturn(List.of(g1, g2));

        List<Group> result = groupService.getAllGroups();

        assertEquals(2, result.size());
        verify(groupRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Should create a new group")
    void createGroup() {
        when(groupRepository.save(g1)).thenReturn(g1);

        Group result = groupService.createGroup(g1);

        assertNotNull(result);
        assertEquals("Admins", result.getGroup_name());
        verify(groupRepository, times(1)).save(g1);
    }

    @Test
    @DisplayName("Should delete a group by ID")
    void deleteGroup() {
        doNothing().when(groupRepository).deleteById(1L);

        groupService.deleteGroup(1L);

        verify(groupRepository, times(1)).deleteById(1L);
    }

    @Test
    @DisplayName("Should update an existing group")
    void updateGroup() {
        Group updatedGroup = new Group(1L, "Super Admins", "Updated description", null, new HashSet<>());
        when(groupRepository.findById(1L)).thenReturn(Optional.of(g1));
        when(groupRepository.save(any(Group.class))).thenReturn(updatedGroup);

        Group result = groupService.updateGroup(1L, updatedGroup);

        assertNotNull(result);
        assertEquals("Super Admins", result.getGroup_name());
        assertEquals("Updated description", result.getGroup_description());
        verify(groupRepository, times(1)).findById(1L);
        verify(groupRepository, times(1)).save(any(Group.class));
    }

    @Test
    @DisplayName("Should add a person to a group")
    void addPersonToGroup() {
        Person person = new Person(1L, "Ola", "Nordmann", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
        when(personRepository.findById(1L)).thenReturn(Optional.of(person));
        when(groupRepository.findById(1L)).thenReturn(Optional.of(g1));
        when(personRepository.save(any(Person.class))).thenReturn(person);

        groupService.addPersonToGroup(1L, 1L);

        assertTrue(person.getGroups().contains(g1));
        verify(personRepository, times(1)).save(person);
    }

    @Test
    @DisplayName("Should remove a person from a group")
    void removePersonFromGroup() {
        Person person = new Person(1L, "Ola", "Nordmann", null, null, null, null, null, null, null, null, new HashSet<>(), new HashSet<>());
        person.getGroups().add(g1);
        when(personRepository.findById(1L)).thenReturn(Optional.of(person));
        when(groupRepository.findById(1L)).thenReturn(Optional.of(g1));
        when(personRepository.save(any(Person.class))).thenReturn(person);

        groupService.removePersonFromGroup(1L, 1L);

        assertFalse(person.getGroups().contains(g1));
        verify(personRepository, times(1)).save(person);
    }
}
