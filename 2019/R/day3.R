
library(magrittr)
library(testthat)

directions <- list(
  U = c(0, 1),
  D = c(0, -1),
  L = c(-1, 0),
  R = c(1, 0)
)

parse_input <- function(input) {
  input %>%
    strsplit(",") %>%
    lapply(
      function(x) {
        list(direction = substring(x, 1, 1),
             units = as.numeric(substring(x, 2)))
      })
}


wires_to_points <- function(wires, direction_map) {
  pts <- wires %>%
    lapply(function(x) {
      direction <- direction_map[x[["direction"]]]
      dims <- seq_along(x[["units"]])
      lapply(dims, function(y) { rep_len(direction[y], length.out = x[["units"]][y]) }) %>%
        Reduce(c, .)
    }) %>%
    lapply(function(x) {
      xn <- cumsum(sapply(x, function(y) { y[1] }))
      yn <- cumsum(sapply(x, function(y) { y[2] }))
      sn <- paste(xn, yn, sep = ",")
      list(x = xn, y = yn, s = sn)
    })
  pts
}


get_wire_crosses <- function(wire_points) {
  wire_points %>%
    lapply(function(x) { x[["s"]] }) %>%
    Reduce(c, .) %>%
    table() %>%
    Filter(function(x) { x > 1 }, .)  #%>%
}


solution <- function(input) {
  wpoints <- wires_to_points(input, directions)
  wcrosses <- get_wire_crosses(wpoints)

  # Validate if crosses are legal
  wvalid <- names(wcrosses) %>%
    lapply(function(x) {
      w1 <- which(wpoints[[1]][["s"]] == x)
      w2 <- which(wpoints[[2]][["s"]] == x)
      list(
        w1 = w1,
        w2 = w2,
        good = length(w1) > 0 & length(w2) > 0
      )
    }) %>%
    set_names(names(wcrosses)) %>%
    Filter(function(x) { x[["good"]] }, .)

  names(wvalid) %>%
    lapply(function(x) { strsplit(x, ",")[[1]] %>% as.numeric() }) %>%
    sapply(function(x) { sum(abs(x)) }) %>%
    min()
}

solution2 <- function(input) {
  wpoints <- wires_to_points(input, directions)
  wcrosses <- get_wire_crosses(wpoints)

  # Validate if crosses are legal
  wvalid <- names(wcrosses) %>%
    lapply(function(x) {
      w1 <- which(wpoints[[1]][["s"]] == x)
      w2 <- which(wpoints[[2]][["s"]] == x)
      list(
        w1 = w1,
        w2 = w2,
        good = length(w1) > 0 & length(w2) > 0
      )
    }) %>%
    set_names(names(wcrosses)) %>%
    Filter(function(x) { x[["good"]] }, .)

  wvalid %>%
    sapply(function(x) { x[["w1"]] + x[["w2"]] }) %>%
    min()
}


test_that("Test Simulations", {
  aa <- c("R8,U5,L5,D3", "U7,R6,D4,L4") %>% parse_input()
  expect_equal(solution(aa), 6)
  expect_equal(solution2(aa), 30)

  aa <- c("R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83") %>% parse_input()
  expect_equal(solution(aa), 159)
  expect_equal(solution2(aa), 610)

  aa <- c("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") %>% parse_input()
  expect_equal(solution(aa), 135)
  expect_equal(solution2(aa), 410)
})


aa <- readLines("../data/data3.txt") %>% parse_input()
solution(aa)
solution2(aa)
