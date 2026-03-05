package com.srib.personaldatabase.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

import java.util.HashSet;
import java.util.Set;
import com.fasterxml.jackson.annotation.JsonIdentityInfo;
import com.fasterxml.jackson.annotation.ObjectIdGenerators;
import jakarta.persistence.ManyToMany;

@Entity
@Data
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "courses")
@EqualsAndHashCode(onlyExplicitlyIncluded = true)
@JsonIdentityInfo(generator = ObjectIdGenerators.PropertyGenerator.class, property = "course_id")
public class Course {
  @Id
  @GeneratedValue(strategy = GenerationType.IDENTITY)
  @EqualsAndHashCode.Include
  private Long course_id;
  private String course_name;
  private String course_description;

  @ManyToMany(mappedBy = "courses")
  private Set<Person> persons = new HashSet<>();

  public Course(String course_name) {
    this.course_name = course_name;
  }

}