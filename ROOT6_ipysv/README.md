## ROOT6 ipython notebook

root 6.26.04 ubuntu22.04

root notebook with the customization for python

* build docker image from [rootproject/root:6.26.04-ubuntu22.04](Dockerfile#L1) with the customization in `Dockerfile`
  ```
  ./build.sh
  ```

* run local ipython notebook server with ROOT6
  ```
  ./run_container.sh
  ```

#### examples
ROOT GUI cannot be displayed via `.ipynb` file from GitHub.  
Viewable html-files for the browser are in [ROOT6_ipysv/WK/examples](WK/examples).  
