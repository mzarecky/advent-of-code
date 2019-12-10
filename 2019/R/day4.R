
library(magrittr)
library(testthat)

convert_password <- function(password) {
  password %>%
    as.character() %>%
    strsplit("") %>%
    extract2(1)
}

validate_password <- function(password) {
  n <- length(password)
  a <- password[seq(1,n-1)]
  b <- password[seq(2,n)]
  increasing <- all(a <= b)
  repeating <- any(a == b)

  increasing & repeating & (n == 6)
}

validate_password2 <- function(password) {
  n <- length(password)
  a <- password[seq(1,n-1)]
  b <- password[seq(2,n)]
  increasing <- all(a <= b)
  dd <- c(FALSE, a==b, FALSE)
  has_doubles <- seq(2,n) %>%
    sapply(function(x) {  all(dd[c(x-1,x,x+1)] == c(FALSE, TRUE, FALSE)) }) %>%
    any()
  increasing & has_doubles & (n == 6)  # & repeating
}


test_that("Check Passwords", {
  password <- convert_password(122345)
  expect_true(validate_password(password))
  expect_true(validate_password2(password))

  password <- convert_password(112233)
  expect_true(validate_password(password))
  expect_true(validate_password2(password))

  password <- convert_password(111123)
  expect_true(validate_password(password))
  expect_false(validate_password2(password))

  password <- convert_password(123444)
  expect_true(validate_password(password))
  expect_false(validate_password2(password))

  password <- convert_password(135679)
  expect_false(validate_password(password))
  expect_false(validate_password2(password))

  password <- convert_password(111111)
  expect_true(validate_password(password))
  expect_false(validate_password2(password))

  password <- convert_password(111122)
  expect_true(validate_password(password))
  expect_true(validate_password2(password))

  password <- convert_password(223450)
  expect_false(validate_password(password))
  expect_false(validate_password2(password))

  password <- convert_password(123789)
  expect_false(validate_password(password))
  expect_false(validate_password2(password))
})


# Data ----
passwords <- readLines("../data/data4.txt") %>%
  strsplit("-") %>%
  extract2(1) %>%
  as.numeric() %>%
  (function(x) { seq(x[1], x[2]) }) %>%
  lapply(convert_password)


# Part 1 ----
Filter(validate_password, passwords) %>% length()

# Part 2 ----
Filter(validate_password2, passwords) %>% length()

