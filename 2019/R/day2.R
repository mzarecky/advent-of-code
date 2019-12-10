
library(magrittr)
library(testthat)

aa <- readLines("../data/data2.txt") %>%
  strsplit(",") %>%
  extract2(1) %>%
  as.numeric()
aa[2] <- 12
aa[3] <- 2


run_simulation <- function(program) {
  current_position <- 0
  while(program[current_position+1] != 99) {
    op <- program[current_position+1]
    val1 <- program[program[current_position+2] + 1]
    val2 <- program[program[current_position+3] + 1]
    pos3 <- program[current_position+4] + 1

    if (op == 1) {
      program[pos3] = val1 + val2
    } else if (op == 2) {
      program[pos3] = val1 * val2
    }
    current_position <- current_position + 4
  }

  program
}


test_that("Test Simulations", {
  aa <- c(1,0,0,0,99)
  expect_equal(c(2,0,0,0,99), run_simulation(aa))

  aa <- c(2,3,0,3,99)
  expect_equal(c(2,3,0,6,99), run_simulation(aa))

  aa <- c(2,4,4,5,99,0)
  expect_equal(c(2,4,4,5,99,9801), run_simulation(aa))

  aa <- c(1,1,1,4,99,5,6,0,99)
  expect_equal(c(30,1,1,4,2,5,6,0,99), run_simulation(aa))

  aa <- c(1,9,10,3,2,3,11,0,99,30,40,50)
  expect_equal(c(3500,9,10,70,2,3,11,0,99,30,40,50), run_simulation(aa))

})

run_simulation(aa)[1]


# Part 2 ----
found <- FALSE
for (noun in 0:99) {
  for (verb in 0:99) {
    aa[2] <- noun
    aa[3] <- verb
    output <- run_simulation(aa) %>% extract(1)
    if (output == 19690720) {
      found <- TRUE
      my_list <- list(noun=noun, verb=verb)
      break
    }
  }
  if (found) { break }
}

100 * my_list[["noun"]] + my_list[["verb"]]
