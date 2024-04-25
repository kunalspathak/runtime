#!/usr/bin/env python3

import os
import subprocess
import sys

def strip_text(text):
    passed_test_index = text.find("Passed test:")
    if passed_test_index != -1:  # If "Passed test:" is found in the text
        return text[passed_test_index:]
    else:
        return text
        
def invoke_test(env_vars, args):
    print(f"------------------- {env_vars} -------------------")
    # Prepare environment variables dictionary
    env = {}
    disable_tiering = True
    for var_name in env_vars:
        if (var_name == 'JitMinOpts') or (var_name == 'TieredCompilation'):
            disable_tiering = False
        env['DOTNET_' + var_name] = env_vars[var_name]

    if disable_tiering:
        env['DOTNET_TieredCompilation'] = '0'

    try:
        # Run the command and capture output and errors
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if 'fail' in result.stdout.lower():
            print("Test failed:")
            output_batch_lines = False
            for line in result.stdout.splitlines():
                if 'failed:' in line:
                    print("..........................................")
                    output_batch_lines = True
                if len(line.strip()) == 0:
                    output_batch_lines = False
                    print("..........................................")
                
                if output_batch_lines or ('System.Exception' in line) or ('at ' in line.strip()):
                    print(line)
        else:
            # Everything passed
            test_count = 0
            for line in result.stdout.splitlines():
                if 'Beginning scenario:' in line:
                    test_count = test_count+1
                if 'Passed test:' in line:
                    print(f'{strip_text(line)} : {test_count}')
                    test_count = 0
                    
        # Print the errors, if any
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error invoking utility: {e}")


test_environments = {
    'default' : [
        {},
    ],
    'jitstress' : [
        {'JitMinOpts': '1'},
        {'JitStress': '1'},
        {'JitStress': '2'},
        {'JitStress': '1', 'TieredCompilation' : '1'},
        {'JitStress': '2', 'TieredCompilation' : '1'},
        {'TailcallStress': '1'},
        {'ReadyToRun': '0'},
    ],
    'jitstressregs' : [
        {'JitStressRegs': '1'},
        {'JitStressRegs': '2'},
        {'JitStressRegs': '3'},
        {'JitStressRegs': '4'},
        {'JitStressRegs': '8'},
        {'JitStressRegs': '0x10'},
        {'JitStressRegs': '0x80'},
        {'JitStressRegs': '0x1000'},
        {'JitStressRegs': '0x2000'},
    ],
    'jitstress2-jitstressregs' : [
        {'JitStress' : '2', 'JitStressRegs' : '1'},
        {'JitStress' : '2', 'JitStressRegs' : '2'},
        {'JitStress' : '2', 'JitStressRegs' : '3'},
        {'JitStress' : '2', 'JitStressRegs' : '4'},
        {'JitStress' : '2', 'JitStressRegs' : '8'},
        {'JitStress' : '2', 'JitStressRegs' : '0x10'},
        {'JitStress' : '2', 'JitStressRegs' : '0x80'},
        {'JitStress' : '2', 'JitStressRegs' : '0x1000'},
        {'JitStress' : '2', 'JitStressRegs' : '0x2000'},
    ]
}

if len(sys.argv) <= 1:
    print("Usage {} test_to_run test_args...".format(sys.argv))
    exit(2)

args = sys.argv[1:]
print(f"Starting test: {' '.join(args)}")

for mode in test_environments:
    print(f"===================Running {mode}===================")
    test_legs = test_environments[mode]
    for test_leg in test_legs:
        invoke_test(test_leg, args)