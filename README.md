# naev
NAEV, or Nonlinear Automatic Equivalent Versioning is an abstraction and tool designed to allow for nonlinear versioning within software. The nonlinear versioning is then automatically verified to be functionally equivalent in the case of non-breaking updates.

# Things that we check
- We only check something if it is exported both when it is initially defined, and in the index.js file. If there is not an index.js file in the root package directory, we will check things exported when they are initially defined from any file in the root directory or the src directory. 
- Classes
    - We check that classes exported in the lower version are also exported in the higher version
    - properties
        - We ignore properties whose name is prefixed with '_' or '#'
        - We check that all non-static properties declared at the top of the class in the lower version are still present in the higher version
        - We check that all static properties declared at the top of the class in the lower version are still present in the higher version
        - We check that any property of the form 'this.*' on the left side of an assignment in any function in the lower version is still present in the higher version
    - functions
        - we ignore functions whose name is prefixed with '_' or '#'
        - We check that all required parameters are the same across both versions
- Variables
    - We check that variables exported in the lower version are also exported in the higher version
- Functions
    - We check that functions exported in the lower version are also exorted in the higher version
    - We check that all required parameters are the same across both versions.