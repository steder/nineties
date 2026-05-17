Feature: A kid checks out an audiobook by voice
  As a kid with a bedside Echo
  I want to ask the Librarian for an available book and start listening
  So that I can fall asleep to a story without an adult mediating

  Background:
    Given the family has a Librarian configured
    And the catalog includes "The Wild Robot" tagged age_floor 6, violence cartoon, themes [bullying]
    And the catalog includes "The Wild Robot Escapes" tagged age_floor 7, violence cartoon
    And the catalog includes "Coraline" tagged age_floor 10, scariness scary
    And "Asher" is a kid age 9 with policy {age_floor max 12, scariness deny scary}
    And "Asher"'s bedside Echo device-id "echo-asher-01" is mapped to "Asher"

  Scenario: Browse available books
    When "Asher" says "Alexa, ask Story Time what books I can check out"
    Then the response lists "The Wild Robot"
    And the response lists "The Wild Robot Escapes"
    And the response does NOT list "Coraline"

  Scenario: Check out a book and start listening
    When "Asher" says "Alexa, ask Story Time to check out The Wild Robot"
    Then a Loan is recorded for "Asher" against "The Wild Robot"
    And the Loan has expires_at within 7 days
    And the response plays a stream URL for "The Wild Robot" at offset 0

  Scenario: Resume a current loan
    Given "Asher" has an active loan for "The Wild Robot" with progress 1845 seconds
    When "Asher" says "Alexa, ask Story Time to read me my book"
    Then the response plays a stream URL for "The Wild Robot" at offset 1845

  Scenario: Loan cap is enforced
    Given "Asher" already has 2 active loans (the family max)
    When "Asher" says "Alexa, ask Story Time to check out The Wild Robot Escapes"
    Then no new Loan is recorded
    And the response explains the loan cap in age-appropriate language

  Scenario: Policy hides ineligible items entirely
    When "Asher" says "Alexa, ask Story Time to check out Coraline"
    Then no Loan is recorded
    And the response says the book is not on the shelf right now
    # NOT "you can't have it" — denial reason is not exposed to the kid.

  Scenario: Returns preserve progress
    Given "Asher" has an active loan for "The Wild Robot" with progress 3120 seconds
    When "Asher" says "Alexa, ask Story Time I'm done with The Wild Robot"
    Then the Loan is returned
    And the Loan's progress_seconds is preserved as 3120
    When "Asher" checks out "The Wild Robot" again after the cooldown
    Then the new Loan resumes playback at offset 3120
