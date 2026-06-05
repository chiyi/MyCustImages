### Example: Create a skill (add-cute-black-cat)

**Testing on Grok Build Beta 0.2.22**

#### Steps

1. **Prepare the prompt file**  
   Create [`create_skill.prmp`](create_skill.prmp) in the project root.
2. **Launch Grok Build and create the Skill**
   ```bash
   cd /work-dir/WK_example
   grok
   ```
3. Once inside Grok Build, run:
   ```
   /model composer-2.5
   ```
   Then paste the following command:
   ```
   Read the entire content of the file "create_skill.prmp" and use it exactly as the prompt to create the reusable Skill "add-cute-black-cat".
   ```
4. Use the SkillAfter creation, you can run:
   ```
   /add-cute-black-cat @pic/inp_image.jpg
   ```

#### Result:
* Generated Skill files:  
  `.grok/skills/add-cute-black-cat` folder
  (includes [SKILL.md](.grok/skills/add-cute-black-cat/SKILL.md))
* Input / Output Example:
  * Original Image:  
    <img src="pic/inp_image.jpg" width="400">  
  * Output:  
    <img src="inp_image_with_cat.jpg" width="400">






_produced by grok_

    
