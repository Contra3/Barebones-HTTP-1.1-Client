# Instructions to submit your homework

- Clone your homework repository
```sh
git clone https://github.com/uic-cs-edu/cs450-net-hw<homework_number>-<yourid>.git
```
- Change your directory to the root directory of the project

```sh
cd cs450-net-hw<homework_number>-<yourid>
```

- Write your netid to the netid file:

Note: If your email address is your_net_id@uic.edu your netid is "your_net_id"

```sh
echo "your_net_id" > netid
```


- Write your code and add your files. 
- Test your program with this command:

```sh
python3 ok --local
```

- If all of the cases are passed, you can push it back to the repository for grading

```sh
git add . 
git commit -m "<add your comment here>" 
git push origin master
```

