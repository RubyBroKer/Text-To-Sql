from graph.workflow import build_graph


graph = build_graph()


question = "Hi"


result = graph.invoke({
    "question": question
})


print(result)