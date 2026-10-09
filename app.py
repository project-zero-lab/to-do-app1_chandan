import streamlit as st
import random

st.title("📝 My To-Do App")
st.write("Manage your daily tasks easily!")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

tasks = st.session_state.tasks


def add_task():
    title = st.session_state.title
    owner = st.session_state.owner
    deadline = st.session_state.deadline
    status = st.session_state.status

    task = {
        "title": title,
        "owner": owner,
        "deadline": str(deadline),
        "done": status
    }

    tasks.append(task)
    st.success("Task added succesfully!")  # Silly mistake 1


def show_tasks():
    if not tasks:
        st.info("No tasks yet.")
        return

    for i, task in enumerate(tasks):
        status_icon = "✅" if task["done"] else "⬜"
        with st.container(border=True):
            st.markdown(f"**{status_icon} {i}. {task['title']}**")
            st.caption(f"Owner: {task['owner']}  |  Deadline: {task['deadline']}")


def remove_task():
    if not tasks:
        st.warning("No tasks available to delete.")
        return

    number = st.number_input(
        "Enter task number to delete",
        min_value=0,
        max_value=len(tasks) - 1,
        step=1
    )

    if st.button("Delete Task"):
        del tasks[number]
        st.success("Task deleted!")
        st.rerun()


def pick_task():
    incomplete_tasks = []

    for task in tasks:
        if task["done"] == False:
            incomplete_tasks.append(task)

    if incomplete_tasks:
        task = random.choice(incomplete_tasks)

        st.info(
            f"Random task: {task['title']} - "
            f"{task['owner']} - Deadline: {task['deadline']}"
        )
    else:
        st.warning("No incomplete task found.")  # Silly mistake 2


st.subheader("➕ Add a New Task")

with st.form("task_form"):
    st.text_input("Task Title", key="title")
    st.text_input("Owner Name", key="owner")
    st.date_input("Deadline", key="deadline")
    st.checkbox("Is the task completed?", key="status")

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if st.session_state.title.strip() and st.session_state.owner.strip():
            add_task()
        else:
            st.error("Please enter the task title and owner.")

st.divider()
st.subheader("📋 Your Tasks")
show_tasks()
