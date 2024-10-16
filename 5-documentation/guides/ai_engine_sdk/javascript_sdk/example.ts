import * as readline from "node:readline";

import {
  AiEngine,
  isAgentMessage,
  isAiEngineMessage,
  isConfirmationMessage,
  isStopMessage,
  isTaskSelectionMessage,
} from "@fetchai/ai-engine-sdk";

const apiKey = process.env["AV_API_KEY"] ?? "";

const snooze = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms));

const main = async () => {
  const rl = readline.promises.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const aiEngine = new AiEngine(apiKey);

  const functionGroups = await aiEngine.getFunctionGroups();
  const publicGroup = functionGroups.find((g) => g.name === "Fetch Verified");
  if (publicGroup === undefined) {
    throw new Error('Could not find "Public" function group.');
  }

  const session = await aiEngine.createsession(publicGroup.uuid);
  await session.start(await rl.question("What is your objective: "));

  try {
    let emptyCount = 0;
    let sessionEnded = false;
    while (emptyCount < 12) {
      const messages = await session.getMessages();
      if (messages.length === 0) {
        emptyCount++;
      } else {
        emptyCount = 0;
      }

      for (const message of messages) {
        if (isTaskSelectionMessage(message)) {
          console.log("Please select a task from the list below:");
          console.log("");
          for (const option of message.options) {
            console.log(`${option.key}: ${option.title}`);
          }

          const optionIndex = parseInt(
            await rl.question("\nEnter task number: "),
          );

          // check the index
          if (optionIndex < 0 || optionIndex >= message.options.length) {
            throw new Error("Invalid task number");
          }

          await session.submitTaskSelection(message, [
            message.options[optionIndex]!,
          ]);
        } else if (isAgentMessage(message)) {
          console.log("Agent: ", message.text);

          const response = await rl.question("User (enter to skip): ");
          if (response === "exit") {
            break;
          }

          if (response !== "") {
            await session.submitResponse(message, response);
          }
        } else if (isAiEngineMessage(message)) {
          console.log("Engine:", message.text);
        } else if (isConfirmationMessage(message)) {
          console.log("Confirm:", message.payload);

          const response = await rl.question(
            "\nPress enter to confirm, otherwise explain issue:\n",
          );

          if (response === "") {
            console.log("Sending confirmation...");
            await session.submitConfirmation(message);
          } else {
            await session.rejectConfirmation(message, response);
          }
        } else if (isStopMessage(message)) {
          console.log("\nSession has ended");
          sessionEnded = true;
          break;
        } else {
          console.error("???", message);
        }
      }

      // if the session has concluded then break
      if (sessionEnded) {
        break;
      }

      await snooze(1200);
    }
  } catch (e) {
    console.error("Error", e);
  } finally {
    // clean up the session
    await session.delete();

    // stop the readline interface
    rl.close();
  }
};

main();