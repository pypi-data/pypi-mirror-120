// Copyright 2019 DeepMind Technologies Ltd. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include "open_spiel/higc/referee.h"

#include "open_spiel/abseil-cpp/absl/flags/flag.h"
#include "open_spiel/abseil-cpp/absl/flags/parse.h"
#include "open_spiel/abseil-cpp/absl/flags/usage.h"

ABSL_FLAG(std::string, bots_dir, "higc/bots",
          "Directory containing the competition bots.");

namespace open_spiel {
namespace higc {
namespace {

void PlaySingleMatchIIGS() {
  std::string bot_first_action =
      absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/test_bot_first_action.sh");
  open_spiel::higc::Referee ref(
      "goofspiel(imp_info=True,points_order=descending)",
      {bot_first_action, bot_first_action}, /*seed=*/42,
      // Increase times for Python scripts.
      TournamentSettings{
          .timeout_ready = 2000,
          .timeout_start = 500,
      });
  SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
  std::unique_ptr<TournamentResults> results = ref.PlayTournament(1);
  SPIEL_CHECK_EQ(results->num_matches(), 1);
  SPIEL_CHECK_TRUE(results->matches[0].terminal->IsTerminal());
  SPIEL_CHECK_EQ(results->matches[0].terminal->HistoryString(),
                 "0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, "
                 "6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11");
}

void TestInvalidBots() {
  std::string bot_first_action =
      absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/test_bot_first_action.sh");
  std::vector<std::string> failing_cases = {"/non_existing_bot",
                                            "/test_bot_with_non_exec_flag"};

  for (const std::string& failing_case : failing_cases) {
    std::cout << "Invalid bot: " << failing_case << std::endl;
    std::string invalid_bot =
        absl::StrCat(absl::GetFlag(FLAGS_bots_dir), failing_case);

    open_spiel::higc::Referee ref("tic_tac_toe",
                                  {invalid_bot, bot_first_action});
    SPIEL_CHECK_FALSE(ref.StartedSuccessfully());
  }
}

void PlayWithFailingBots() {
  std::vector<std::string> failing_cases = {
      "/test_bot_break_pipe.sh",     "/test_bot_sleep.sh",
      "/test_bot_ready.sh",          "/test_bot_start.sh",
      "/test_bot_illegal_action.sh",
      //      "/test_bot_buffer_overflow.sh",
  };

  for (int i = 0; i < failing_cases.size(); ++i) {
    const std::string& failing_case = failing_cases[i];
    std::string failing_bot =
        absl::StrCat(absl::GetFlag(FLAGS_bots_dir), failing_case);
    std::cout << "\n\nFailing bot: " << failing_bot << std::endl;

    // Use a single-player game.
    open_spiel::higc::Referee ref(
        "cliff_walking", {failing_bot}, /*seed=*/42,
        /*settings=*/
        TournamentSettings{// Disqualify after the 2nd failing match.
                           .disqualification_rate = 0.5});
    SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
    std::unique_ptr<TournamentResults> results = ref.PlayTournament(2);
    SPIEL_CHECK_EQ(results->disqualified[0], true);
    if (i < 2) {
      // No matches are played, if the bot can't even start properly.
      SPIEL_CHECK_EQ(results->num_matches(), 0);
    } else {
      SPIEL_CHECK_EQ(results->num_matches(), 2);
    }
  }
}

void PlayWithSometimesFailingBot() {
  std::string failing_bot = absl::StrCat(absl::GetFlag(FLAGS_bots_dir),
                                         "/test_bot_fail_after_few_actions.sh");
  std::cout << "\n\nFailing bot: " << failing_bot << std::endl;

  // Use a single-player game.
  open_spiel::higc::Referee ref("cliff_walking", {failing_bot}, /*seed=*/42,
                                /*settings=*/
                                TournamentSettings{
                                    // Increase times for Python scripts.
                                    .timeout_ready = 2000,
                                    .timeout_start = 500,
                                    // Disqualify after the 2nd failing match.
                                    .disqualification_rate = 0.5,
                                });
  SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
  std::unique_ptr<TournamentResults> results = ref.PlayTournament(2);
  SPIEL_CHECK_EQ(results->disqualified[0], true);
  SPIEL_CHECK_EQ(results->num_matches(), 2);
}

void PonderActTimeout() {
  open_spiel::higc::Referee ref(
      "leduc_poker",
      {absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/random_bot_py.sh"),
       absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/test_bot_start.sh")},
      /*seed=*/42,
      // Increase times for Python scripts.
      TournamentSettings{
          .timeout_ready = 2000,
          .timeout_start = 500,
      });
  SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
  std::unique_ptr<TournamentResults> results = ref.PlayTournament(1);
  SPIEL_CHECK_EQ(results->num_matches(), 1);
}

void PlayManyRandomMatches(int num_matches = 5) {
  open_spiel::higc::Referee ref(
      "leduc_poker",
      {absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/random_bot_py.sh"),
       absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/random_bot_cpp.sh")},
      /*seed=*/42,
      // Increase times for Python scripts.
      TournamentSettings{
          .timeout_ready = 2000,
          .timeout_start = 500,
      });
  SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
  std::unique_ptr<TournamentResults> results = ref.PlayTournament(num_matches);
  SPIEL_CHECK_EQ(results->num_matches(), num_matches);
  results->PrintCsv(std::cout, /*print_header=*/true);
}

void PlayWithManyPlayers() {
  constexpr const int num_bots = 8;
  std::vector<std::string> bots;
  for (int i = 0; i < num_bots; ++i) {
    bots.push_back(
        absl::StrCat(absl::GetFlag(FLAGS_bots_dir), "/random_bot_cpp.sh"));
  }
  open_spiel::higc::Referee ref(
      absl::StrCat("goofspiel(players=", num_bots,
                   ",imp_info=True,points_order=descending)"),
      bots,
      /*seed=*/42,
      // Increase times for Python scripts.
      TournamentSettings{
          .timeout_ready = 2000,
          .timeout_start = 500,
      });
  SPIEL_CHECK_TRUE(ref.StartedSuccessfully());
  std::unique_ptr<TournamentResults> results = ref.PlayTournament(1);
  SPIEL_CHECK_EQ(results->num_matches(), 1);
}

}  // namespace
}  // namespace higc
}  // namespace open_spiel

// Reroute the SIGPIPE signall here, so the test pass ok.
void signal_callback_handler(int signum) {
  std::cout << "Caught signal SIGPIPE " << signum << std::endl;
}

int main(int argc, char** argv) {
  absl::ParseCommandLine(argc, argv);
  signal(SIGPIPE, signal_callback_handler);

  open_spiel::higc::TestInvalidBots();
  open_spiel::higc::PlayWithFailingBots();
  open_spiel::higc::PlayWithSometimesFailingBot();
  open_spiel::higc::PonderActTimeout();
  open_spiel::higc::PlayWithManyPlayers();
  open_spiel::higc::PlaySingleMatchIIGS();
  open_spiel::higc::PlayManyRandomMatches();
}
