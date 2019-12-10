
library(magrittr)
library(testthat)
library(data.table)

options(stringsAsFactors = FALSE)



parse_orbits <- function(x) {
  x %>%
    strsplit(")") %>%
    lapply(function(y) { list(parent=y[[1]], child=y[[2]]) })
}

get_all_objects <- function(om) {
  c(sapply(om, function(x) { x[["parent"]] }),
    sapply(om, function(x) { x[["child"]] })) %>%
  unique()
}

find_head <- function(om) {
  setdiff(
    unique(sapply(om, function(x) { x[["parent"]] })),
    unique(sapply(om, function(x) { x[["child"]] }))
  )
}

create_child_map <- function(om) {
  ao <- get_all_objects(om)
  ao %>%
    lapply(function(x) {
      aa <- Filter(function(y) { y[["parent"]] == x }, om) %>%
        sapply(function(y) { y[["child"]] })
      if (length(aa) == 0) {
        aa <- character(0)
      }
      aa
    }) %>%
    set_names(ao)
}

create_parent_map <- function(om) {
  ao <- get_all_objects(om)
  ao %>%
    lapply(function(x) {
      aa <- Filter(function(y) { y[["child"]] == x }, om) %>%
        sapply(function(y) { y[["parent"]] })
      if (length(aa) == 0) {
        aa <- character(0)
      }
      aa
    }) %>%
    set_names(ao)
}

get_children <- function(cm, p) {
  lapply(p, function(x) { cm[[x]] }) %>%
    Reduce(c, .) %>%
    unique()
}

get_number_orbits <- function(om) {
  obj <- get_all_objects(om)
  heads <- find_head(om)
  cm <- create_child_map(om)
  level <- 0

  output <- lapply(obj, function(x) { level }) %>% set_names(obj)
  current_children <- get_children(cm, heads)
  while (length(current_children) > 0) {
    level <- level + 1
    for (j in current_children) {
      output[[j]] <- level
    }
    current_children <- get_children(cm, current_children)
  }

  output
}

get_parent_tree <- function(om, node, pm = NULL) {
  if (is.null(pm)) {
    pm <- create_parent_map(om)
  }
  output <- node

  parent <- pm[[node]]
  while (length(parent) > 0) {
    output <- c(output, parent)
    parent <- pm[[parent]]
  }
  output
}


solution1 <- function(om) {
  get_number_orbits(om) %>%
    sapply(function(x) { x[[1]] }) %>%
    sum()
}


solution2 <- function(om, node1, node2) {
  orbit_levels <- get_number_orbits(om)
  you_map <- get_parent_tree(om, node1)
  san_map <- get_parent_tree(om, node2)

  same_nodes <- intersect(you_map, san_map)
  common_node <- same_nodes %>%
    Filter(function(x) {
      big_level <- same_nodes %>%
        sapply(function(y) { orbit_levels[[y]] }) %>%
        max()
      orbit_levels[[x]] == big_level
    }, .)

  orbit_levels[[node2]] + orbit_levels[[node1]] - 2 * orbit_levels[[common_node]] - 2
}



test_that("Check Orbits", {
  aa <- c("COM)B", "B)C", "C)D", "D)E", "E)F", "B)G",
          "G)H", "D)I", "E)J", "J)K", "K)L")
  my_orbits <- aa %>% parse_orbits()


  expect_equal(solution1(my_orbits), 42)

  aa <- c("COM)B", "B)C", "C)D", "D)E", "E)F", "B)G",
          "G)H", "D)I", "E)J", "J)K", "K)L", "K)YOU", "I)SAN")

  my_orbits <- aa %>% parse_orbits()
  expect_equal(solution2(my_orbits, "YOU", "SAN"), 4)
})


# Part 1 ----
aa <- readLines("../data/data6.txt")
my_orbits <- aa %>% parse_orbits()
solution1(my_orbits)


# Part 2 ----
solution2(my_orbits, "YOU", "SAN")

