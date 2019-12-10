
library(magrittr)
library(testthat)

aa <- read.delim(
  "../data/data1.txt",
  header = FALSE,
  colClasses = "numeric",
  col.names = "module"
)


get_fuel_requirement <- function(x) { pmax(floor(x/3) - 2, 0) }

get_fuel_requirement_recursive <- function(x) {
  fuel <- numeric(length(x))
  while (any(x > 6)) {
    x <- sapply(x, get_fuel_requirement)
    fuel <- fuel + x
  }
  fuel
}

get_fuel_sum <- function(x) {
  x[["module"]] %>% get_fuel_requirement() %>% sum()
}

get_fuel_sum_recursive <- function(x) {
  x[["module"]] %>% get_fuel_requirement_recursive() %>% sum()
}

test_that("Unit Tests Part 1", {
  expect_equal(get_fuel_requirement(12), 2)
  expect_equal(get_fuel_requirement(14), 2)
  expect_equal(get_fuel_requirement(1969), 654)
  expect_equal(get_fuel_requirement(100756), 33583)
})

test_that("Unit Tests Part 2", {
  expect_equal(get_fuel_requirement_recursive(14), 2)
  expect_equal(get_fuel_requirement_recursive(1969), 966)
  expect_equal(get_fuel_requirement_recursive(100756), 50346)

  expect_equal(get_fuel_requirement_recursive(c(14,1969,100756)), c(2,966,50346))
})

get_fuel_sum(aa)
get_fuel_sum_recursive(aa)
