import sys
import subprocess
import os

# scripts/orchestrator.py (Enhanced with real-time logging)
# Orchestrates the implementation-review loop between Claude and Codex.

def run_agent(agent, prompt, options=""):
    print(f"\n>>> Calling {agent.upper()}...", flush=True)
    wrapper = os.path.join(os.path.dirname(__file__), "agent-wrapper.sh")
    
    try:
        # Using check=True and merging stderr to see if something crashes
        result = subprocess.run(
            ["bash", wrapper, agent, prompt, options], 
            capture_output=True, 
            text=True
        )
        
        if result.returncode != 0:
            print(f"!!! Error from {agent}: {result.stderr}", flush=True)
            return None
            
        output = result.stdout.strip()
        # Preview first 100 chars of output to confirm progress
        preview = (output[:100] + '...') if len(output) > 100 else output
        print(f"<<< {agent.upper()} Finished. (Output length: {len(output)})", flush=True)
        return output
    except Exception as e:
        print(f"!!! Exception running {agent}: {e}", flush=True)
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 orchestrator.py '<task_description>'")
        sys.exit(1)

    task = sys.argv[1]
    max_loops = 3
    
    print(f"=== CLAUDE-CODEX COLLABORATION START ===", flush=True)
    print(f"Task: {task}", flush=True)
    
    # 1. Implementation Phase (Claude)
    impl_prompt = f"Implementation Task: {task}. Please implement the code and output the full source code inside code blocks."
    implementation = run_agent("claude", impl_prompt)
    
    if not implementation:
        print("Initial implementation failed. Aborting.", flush=True)
        return

    for i in range(max_loops):
        print(f"\n--- Collaboration Loop {i+1}/{max_loops} ---", flush=True)
        
        # 2. Review Phase (Codex)
        review_prompt = f"Original Task: {task}\n\nCode implemented by Claude:\n{implementation}\n\nCritically review this code for bugs, security, and best practices. If no critical issues are found, start your response with 'LGTM'."
        review = run_agent("codex", review_prompt)
        
        if not review:
            print("Review phase failed. Stopping loop.", flush=True)
            break

        if "LGTM" in review.upper():
            print("Codex Review: LGTM (Looks Good To Me).", flush=True)
            break
            
        print(f"Codex Review: Issues found. Requesting refinement from Claude.", flush=True)
        
        # 3. Refinement Phase (Claude)
        refine_prompt = f"Original Task: {task}\nPrevious Implementation:\n{implementation}\n\nCodex Review Feedback:\n{review}\n\nPlease address the feedback and provide the updated source code."
        updated_implementation = run_agent("claude", refine_prompt)
        
        if updated_implementation:
            implementation = updated_implementation
        else:
            print("Refinement failed. Sticking with previous version.", flush=True)
            break

    print(f"\n=== COLLABORATION COMPLETE ===", flush=True)
    print("\n[FINAL SOURCE CODE]")
    print(implementation)

if __name__ == "__main__":
    main()
