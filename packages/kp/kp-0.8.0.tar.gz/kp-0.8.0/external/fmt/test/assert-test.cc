// Formatting library for C++ - FMT_ASSERT test
//
// It is a separate test to minimize the number of EXPECT_DEBUG_DEATH checks
// which are slow on some platforms. In other tests FMT_ASSERT is made to throw
// an exception which is much faster and easier to check.
//
// Copyright (c) 2012 - present, Victor Zverovich
// All rights reserved.
//
// For the license information refer to format.h.

#include "fmt/core.h"
#include "gtest.h"

TEST(AssertTest, Fail) {
#if GTEST_HAS_DEATH_TEST
  EXPECT_DEBUG_DEATH(FMT_ASSERT(false, "don't panic!"), "don't panic!");
#else
  fmt::print("warning: death tests are not supported\n");
#endif
}

bool test_condition = false;

TEST(AssertTest, DanglingElse) {
  bool executed_else = false;
  if (test_condition)
    FMT_ASSERT(true, "");
  else
    executed_else = true;
  EXPECT_TRUE(executed_else);
}
