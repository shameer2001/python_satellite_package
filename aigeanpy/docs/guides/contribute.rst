How to Contribute to this Package
===================================

Prerequisites
-------------

If you don't already have 'git' installed and setup:
    - Download and install the latest version of git.
    - Open a 'git bash' window.
    - Configure git with your "username" and "email":

    .. code-block:: text

        $ git config --global user.name 'your name'
        $ git config --global user.email 'your email'


If you don't already have 'GitHub' and setup:
    - Create a GitHub account.

    


Development Process
-------------------

Setting up the development process:

    - Fork the main repository found at https://github.com/UCL-COMP0233-22-23/aigeanpy-Working-Group-01 by clicking the "fork" button.

    - Clone this fork to your local computer:

    .. code-block:: text

        $ git clone https://github.com/your-username/aigeanpy-Working-Group-01.git



    - Change the directory to the package folder:


    .. code-block:: text

        $ cd aigeanpy

    - Pull the latest changes from upstream:



    .. code-block:: text

        $ git checkout main
        $ git pull upstream main



    - Create a branch to identify your name and the contribution you are making. E.G. 'bob_improve_speed'.

    .. code-block:: text

        $ git branch <name_contribution>
        $ git checkout <name_contribution>



Develop your contribution:

    - Using an IDE (Integrated Development Environment) or an editor, make the contribution and commit locally as you advance.

    - Ensure the commit message is properly formatted and detailed enough; include what change you made and, briefly, what it does.

    - Include tests that will pass after you make your change and fails without the change. 


Submit your changes:

    - Push your changes back onto GitHub to your fork:

    .. code-block:: text

        $ git push origin <name_contribution>

    - Click the green 'pull request' button on the forked repository on your GitHub account to open a pull request. Make the title and message clear. This will be used to explain your changes. Then click the submit button.

    - Someone on our team will review your pull request to ensure the changes made are correct and a worthy improvement.



How to Test your Code
---------------------

- Ensure you have pytest installed.
- Create a separate python document to your contribution with and appropriate name.
- Import 'pyest' into that python document.
- Create functions beginning with `test_` that will test that the contributions you've made are as expected. For example:

.. code-block:: text
    
    def test_addition():
      
       result = addition(1,1)
       expected = 2

       assert result == expected


- You can also create 'negative tests' which will ensure that error messages present in your contribution will show up if the conditions are met.
- Run pytest in the terminal once completed:

.. code-block:: text 

    $ python -m pytest




Code Style
----------

Your code should be clear and concise. Follow the 'PEP 8' style of writing code. 
Ensure there are comments to explain clearly what you're doing. 
Ensure there are docstrings in 'numpy format' to explain any functions you create.