import dotenv from "dotenv";
dotenv.config();

import { query, type SDKMessage } from "@anthropic-ai/claude-code";
import { systemPrompt, testOutputClaude, userPrompt } from "./constants.js";
import { processWithStructuredOutput } from "./openai-processor.js";
import { createOliveIntegration } from "./olive-integration.js";
import fs from "fs";
import path from "path";

const args = process.argv.slice(2);
if (args.length < 2) {
  console.error('Usage: pnpm dev <company_name> <website_to_build>');
  process.exit(1);
}
export const company_name = args[0] as string;
const website_to_build = args[1] as string;

const dataDir = path.join(process.cwd(), "data");

function saveClaudeOutput(claudeOutput: any, companyName: string) {
    const fileName = `${companyName.toLowerCase()}.json`;
    const filePath = path.join(dataDir, fileName);
    fs.writeFileSync(filePath, JSON.stringify(claudeOutput, null, 2));
}

function loadExistingClaudeOutput(companyName: string): any | null {
  try {
    // Get all JSON files in the data directory
    const files = fs.readdirSync(dataDir)
    for (const file of files) {
      const fileNameWithoutExtension = file.replace('.json', '');
      
      // Check if filename is contained within company_name
      if (companyName.toLowerCase().includes(fileNameWithoutExtension.toLowerCase())) {
        const filePath = path.join(dataDir, file);
        const fileContent = fs.readFileSync(filePath, 'utf-8');
        const claudeOutput = JSON.parse(fileContent);
        console.log(`Found matching Claude output for ${companyName}: ${filePath}`);
        return claudeOutput;
      }
    }
    return null;
  } catch (error) {
    console.error("Error loading existing Claude output:", error);
    return null;
  }
}

async function main() {
    const messages: SDKMessage[] = [];
    let claudeOutput: any = null;

    try {
      claudeOutput = loadExistingClaudeOutput(company_name);
      
      if (!claudeOutput) {
        // Step 1: Get output from Claude Code SDK with Neon MCP
        for await (const message of query({
        prompt: `${userPrompt({ website: website_to_build })}`,
        options: {
          appendSystemPrompt: systemPrompt,
          permissionMode: 'bypassPermissions',
          maxTurns: 100,
          mcpServers: {
            "neon": {
              "command": "npx",
              "args": [
                "-y",
                "@neondatabase/mcp-server-neon",
                "start",
                "napi_17j5cpiaia7ii4n95al28nlf44xchrtyzu5gpbseo43o0swksfsp373jv54uabnf"
              ]
            }
          }
        },
      })) {
        messages.push(message);
        console.dir(message, { depth: null });
        
        // Try to extract JSON from assistant messages
        if (message.type === 'assistant' && message.message?.content) {
          const content = typeof message.message.content === 'string' 
            ? message.message.content 
            : message.message.content.map((c: any) => c.type === 'text' ? c.text : '').join('');
          
          // Look for JSON in the message
          const jsonMatch = content.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            try {
              claudeOutput = JSON.parse(jsonMatch[0]);
              console.log("Extracted Claude Output:", claudeOutput);
            } catch (e) {
              console.log("Failed to parse JSON from Claude response");
            }
          }
        }
      }
      saveClaudeOutput(claudeOutput, company_name);
    } 

    // Step 2: Process with OpenAI structured output
    if (claudeOutput) {
      console.log("Processing with OpenAI structured output...");
      
      const structuredResult = await processWithStructuredOutput(
        claudeOutput
      );
      
      console.log("Final Structured Output:");
      console.log(JSON.stringify(structuredResult, null, 2));
      
      // Step 3: Create Olive Integration
      console.log("Starting Olive integration...");
      await createOliveIntegration(structuredResult);
      
      return structuredResult;
    } else {
      console.log("No Claude output found, cannot proceed with processing");
      return null;
    }

    } catch (error) {
      console.error(`error building database for ${website_to_build}:`, error);
      throw error;
    }
}

main();
// (async () => {
//   const structuredOutput = await processWithStructuredOutput(testOutputClaude);
//   await createOliveIntegration(structuredOutput);
// })();