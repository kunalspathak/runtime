sve_api contents

**out_api/**
  All the SVE API designs under review on github. Each file is a separate
  github issue, and contains all three sections used in review:
- API in summary T format
- full API
- rejected methods

**out_cs_api/**
  The full API files that will be put in
  src/libraries/System.Private.CoreLib/src/System/Runtime/Intrinsics/Arm
  Also includes separate files for each section that needs adding to
  src/libraries/System.Runtime.Intrinsics/ref/System.Runtime.Intrinsics.cs

**out_helper_api/**
  The full API with extra information in the summary for development help
- Instructions used by each C ACLE method (as per ACLE spec)
- Entries from codegenarm64test for each instruction mentioned
- If the API has an embedded mask required to mask the result

**out_hwintrinsiclistarm64sve.h**
  The entire file for src/coreclr/jit/hwintrinsiclistarm64sve.h
  The category and flags fields will need manually updating.
  Entires with multiple instructions per type will need to pick one and then
  use a mnually written sepcial encoding.

**out_GenerateHWIntrinsicTests_Arm.cs**
  All the entries for the SVE table in
  src/tests/Common/GenerateHWIntrinsicTests/GenerateHWIntrinsicTests_Arm.cs
  This includes all argument parameters, but is missing fields for validating
  output or any other specialised handling.
  There is one template per API entry - developers are encouraged to use
  more generic template names.

**out_markdownlist.md**
  A checklist of all API methods

**post_review/**
  A copy of each API that was reviewed and approved on github, plus an
  alpahabetically sorted copy. Ideally there should be no difference between
  the sorted files and the versions in out_api/, however there are known issues.
