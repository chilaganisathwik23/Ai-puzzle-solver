from collections import deque
import sys


import flet as ft


#-----------------------------------------------------------------------------
     #Manhattan distance for finding distance b/w current and goal state
#-----------------------------------------------------------------------------


def manhattan(state,goal):
    dis=0
    for i in range(9):
        if state[i]!=0:
            curr_row=i//3
            curr_col=i%3

            goal_ind=goal.index(state[i])
            goal_row=goal_ind//3
            goal_col=goal_ind%3
            dis+=abs(curr_row-goal_row)+abs(curr_col-goal_col)

    return dis


#-----------------------------------------------------------------------------
     #To get all possible states
#-----------------------------------------------------------------------------

def get_neighbours(list):
    neighbours=[]
    
    for i in range(len(list)):
       if list[i]==0:
           x=i
           break
        
    #Left
    if x%3!=0:
        newlist = list.copy()
        temp=newlist[x]
        newlist[x]=newlist[x-1]
        newlist[x-1]=temp
        neighbours.append(newlist)
        
    #Right
    if x%3!=2:
        newlist = list.copy()
        temp=newlist[x]
        newlist[x]=newlist[x+1]
        newlist[x+1]=temp
        neighbours.append(newlist)

    #Up
    if x>=3:
        newlist = list.copy()
        temp=newlist[x]
        newlist[x]=newlist[x-3]
        newlist[x-3]=temp
        neighbours.append(newlist)
        
    #Down    
    if x<6:
        newlist = list.copy()
        temp=newlist[x]
        newlist[x]=newlist[x+3]
        newlist[x+3]=temp
        neighbours.append(newlist)

    return neighbours



#-----------------------------------------------------------------------------
     #BFS
#-----------------------------------------------------------------------------


        
def BFS(start,goal):
    visited=[]
    visited.append(start)
    queue=deque()
    queue.append(start)
    paths=[[start]]

    while queue:
        current=queue.popleft()
        current_path=paths.pop(0)

        if current==goal:
            return current_path

        neighbours=get_neighbours(current)
        for nextstate in neighbours:
             if nextstate not in visited:
                 visited.append(nextstate)
                 queue.append(nextstate)
                 newpath=current_path+[nextstate]
                 paths.append(newpath)


       
    return None           


#-----------------------------------------------------------------------------
     #DFS
#-----------------------------------------------------------------------------        

def DFS(start, goal):
    visited = set()
    stack = [(start, [start])]

    while stack:
        current, current_path = stack.pop()

        if current == goal:
            return current_path

        current_key = tuple(current)

        if current_key not in visited:
            visited.add(current_key)

            neighbours = get_neighbours(current)

            for nextstate in reversed(neighbours):
                if tuple(nextstate) not in visited:
                    newpath = current_path + [nextstate]
                    stack.append((nextstate, newpath))

    return None


#-----------------------------------------------------------------------------
     #Greedy best first search
#-----------------------------------------------------------------------------
def greedy(start,goal):
    open=[start]
    paths=[[start]]
    visited=[]
    current_state=start
    current=100000000

    while open:
        current=100000000

        for i in range(len(open)):
            node = open[i]
            temp=manhattan(node,goal)

            if current>temp:
                current=temp
                current_state=node
                current_path=paths[i]

                
        if current_state==goal:
            return current_path

        index=open.index(current_state)
        
        open.remove(current_state)
        paths.pop(index)
        
        if current_state not in visited:
            visited.append(current_state)

            neighbours=get_neighbours(current_state)

            for nextstate in neighbours:
                if nextstate not in visited and nextstate not in open:
                    open.append(nextstate)
                    newpath=current_path+[nextstate]
                    paths.append(newpath)


    return None



#-----------------------------------------------------------------------------
     #Astar
#-----------------------------------------------------------------------------

def astar(start,goal):
    open=[start]
    costs=[0]
    paths=[[start]]
    visited=[]
    current_state=start
    current=100000000

    while open:
        current=100000000

        for i in range(len(open)):
            temp=costs[i]+manhattan(open[i],goal)

            if current>temp:
                current=temp
                current_state=open[i]
                current_cost=costs[i]
                current_path=paths[i]

        if current_state==goal:
            return current_path

        index=open.index(current_state)
        open.remove(current_state)
        costs.pop(index)
        paths.pop(index)

        if current_state not in visited:
             visited.append(current_state)

             neighbours=get_neighbours(current_state)

             for nextstate in neighbours:
                 newcost=current_cost+1
                 newpath=current_path+[nextstate]
                 
                 if nextstate not in visited:
                     if nextstate not in open:
                         open.append(nextstate)
                         costs.append(newcost)
                         paths.append(newpath)

                     else:
                         index=open.index(nextstate)

                         if newcost<costs[index]:
                             costs[index]=newcost
                             paths[index]=newpath

    return None


#----------------------------------------------------------------------------
     #board creation
#----------------------------------------------------------------------------

def create_board(state):
    rows=[]

    for i in range(0,9,3):
        cells=[]
        for j in range(i,i+3):
            value=state[j]

            if value==0:
                text=" "
            else:
                text=str(value)

            if value==0:
                cells.append(
                ft.Container(
                    content=ft.Text(
                        text,
                        size=25,
                        text_align=ft.TextAlign.CENTER
                        ),
                    width=65,
                    height=65,
                    alignment=ft.Alignment.CENTER,
                    bgcolor="yellow",
                    border=ft.Border(
                        left=ft.BorderSide(width=3),
                        right=ft.BorderSide(width=3),
                        top=ft.BorderSide(width=3),
                        bottom=ft.BorderSide(width=3)
                        ),
                    border_radius=8
                    )
                )

            else:

                cells.append(
                    ft.Container(
                        content=ft.Text(
                            text,
                            size=25,
                            text_align=ft.TextAlign.CENTER
                            ),
                        width=65,
                        height=65,
                        alignment=ft.Alignment.CENTER,
                        bgcolor="yellow",
                        border=ft.Border(
                        left=ft.BorderSide(width=1),
                        right=ft.BorderSide(width=1),
                        top=ft.BorderSide(width=1),
                        bottom=ft.BorderSide(width=1)
                        ),
                        border_radius=8
                        )
                    )
                        

        rows.append(
                ft.Row(
                    controls=cells,
                    alignment=ft.MainAxisAlignment.CENTER
                    )
                )

    return ft.Column(
        controls=rows,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

        
                        

#----------------------------------------------------------------------------
     #for reading input
#----------------------------------------------------------------------------


def read_boxes(boxes):
     values=[]

     for box in boxes:

         if box.value is None or box.value.strip()=="":
             return None

         try:
             value=int(box.value)

         except:
             return None

         values.append(value)

     return values




#----------------------------------------------------------------------------
     #checking validity of puzzle
#----------------------------------------------------------------------------

def valid_state(state):
     if len(state)!=9:
         return False

     if sorted(state)!=[0,1,2,3,4,5,6,7,8]:
         return False

     return True


#----------------------------------------------------------------------------
     #checking it is solavable or not
#----------------------------------------------------------------------------

def is_solvable(start, goal):
    start_tiles = [n for n in start if n != 0]
    goal_tiles = [n for n in goal if n != 0]

    start_inversions = 0
    goal_inversions = 0

    for i in range(8):
        for j in range(i + 1, 8):
            if start_tiles[i] > start_tiles[j]:
                start_inversions += 1

            if goal_tiles[i] > goal_tiles[j]:
                goal_inversions += 1

    return start_inversions % 2 == goal_inversions % 2


#----------------------------------------------------------------------------
     #dispaly
#----------------------------------------------------------------------------

def display(result_area,path,algorithm):
    
    result_area.controls.clear()

    result_area.controls.append(
        ft.Text(
            "Total Moves: "+str(len(path)-1),
            size=18
            )
        )

    result_area.controls.append(
        ft.Text(
            algorithm+" Solution Path",
            size=25
            )
        )

    for i in range(len(path)):

       result_area.controls.append(
           ft.Text(
               "Step "+str(i+1),
               size=18
               )
           )
       result_area.controls.append(
           create_board(path[i])
           )

       if i!=len(path)-1:

           result_area.controls.append(
               ft.Text( "↓",size=30)
               )
           
                   
    
    result_area.update()




#----------------------------------------------------------------------------
     #Main gui
#----------------------------------------------------------------------------

def main(page):
    page.title="AI Puzzle Solver & Search Algorithm visualizer"
    page.scroll=ft.ScrollMode.AUTO
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    #Title

    page.add(
        ft.Text(
            "AI Puzzle Solver & Search Algorithm visualizer",
            size=28
            )
        )
    
    page.add(
        ft.Text(
            "Enter numbers 0-8. Use 0 for the blank space!!!",
            size=16
            )
        )

    #start state

    page.add(
        ft.Text(
            "Start State",
            size=22
            )
        )
    start_boxes=[]

    for i in range(9):

        box=ft.TextField(
            width=60,
            height=60,
            text_size=22,
            text_align=ft.TextAlign.CENTER
            )
        start_boxes.append(box)

    for i in range(0,9,3):
        page.add(
            ft.Row(
                controls=[
                    start_boxes[i],
                    start_boxes[i+1],
                    start_boxes[i+2]
                ],
                alignment=ft.MainAxisAlignment.CENTER

                )
            )


    #goal state

    page.add(
        ft.Text(
            "Goal State",
            size=22
            )
        )

    goal_boxes=[]

    for i in range(9):

        box=ft.TextField(
            width=60,
            height=60,
            text_size=22,
            text_align=ft.TextAlign.CENTER
            )
        goal_boxes.append(box)

    for i in range(0,9,3):
        page.add(
            ft.Row(
                controls=[
                    goal_boxes[i],
                    goal_boxes[i+1],
                    goal_boxes[i+2]
                ],
                alignment=ft.MainAxisAlignment.CENTER

                )
            )


    #Alogorithm selection


    algorithm=ft.Dropdown(
        label="Choose Algorithm",
        width=250,
        value="BFS",
        options=[
            ft.DropdownOption(
                key="BFS",
                text="BFS"
                ),
            ft.DropdownOption(
                key="DFS",
                text="DFS"
                ),
            ft.DropdownOption(
                key="Greedy",
                text="Greedy Best-First Search"
                ),
            ft.DropdownOption(
                key="A*",
                text="A* Search"
                ),
            ]
        )

    page.add(algorithm)


    #result area
    result_area=ft.Column()


    #solve fun

    def solve(e):
        start=read_boxes(start_boxes)
        goal=read_boxes(goal_boxes)

        #check input
        if start is None or goal is None:
            result_area.controls.clear()

            result_area.controls.append(
                ft.Text(
                    "Please Enter All 9 Values.!!!",
                    size=18
                    )
                )
            result_area.update()
            
            return


        if not valid_state(start) or not valid_state(goal):
           

           result_area.controls.clear()
           result_area.controls.append(
              ft.Text(
                  "Invalid Input!",
                  size=18
                )
            )
           result_area.controls.append(
              ft.Text(
                  "Use Every number from 0 to 8 exactly Once.",
                  size=16
                )
            )
           result_area.update()

           return

        selected=algorithm.value

        
        if not is_solvable(start, goal):
            result_area.controls.clear()
            result_area.controls.append(
                ft.Text(
                    "This puzzle cannot reach the selected goal state.",
                    size=18
                )
            )
            result_area.update()
            return


        #run selected algo

        if selected=="BFS":     
           path=BFS(start,goal)

        elif selected=="DFS":
           path=DFS(start,goal)

        elif selected=="Greedy":
           path=greedy(start,goal)

        elif selected=="A*":
           path=astar(start,goal)

        else:
           path=None
           

        #display

        if path is None:
           result_area.controls.clear()
           result_area.controls.append(
               ft.Text(
                   "No Solution found.",
                   size=25
                )
            )
           result_area.update()

        else:
           display(result_area,path,selected)


    #solve btn

    page.add(
        ft.Button(
            content="Solve Puzzle",
            on_click=solve
            )
        )

    page.add(
        ft.Divider()
        )

    page.add(result_area)


ft.run(main)

        

     






















