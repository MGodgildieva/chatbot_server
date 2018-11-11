from datetime import datetime

from django.http import JsonResponse

from appserver.models import *


def register_user(username, email, password, lang):
    check_user = User.objects.filter(email=email)
    if check_user:
        return JsonResponse({'success':  False, 'message': "There is a user with this email"}, status=400)
    new_user = User(first_name=username, email=email, password=password, lang=lang, last_active=date.today())
    new_user.save()
    return JsonResponse({'success':  True, 'message': new_user.register_info()})


def register_child(firstname, parent_id, birthday):
    parent = User.objects.get(pk=parent_id)
    date_birthday = datetime.strptime(birthday, "%d/%m/%Y").date()
    #existing_child = Child.objects.filter(first_name=firstname, parent=parent, birthday=date_birthday)
    existing_child = Child.objects.filter(first_name=firstname, parent=parent_id, birthday=date_birthday)
    if existing_child:
        return JsonResponse({'success': False, 'message': "You already have a child with the same name and the same birthday"}, status=400)
    new_child = Child(first_name=firstname, parent=parent_id, birthday=date_birthday, last_active=date.today())
    #new_child = Child(first_name=firstname, parent=parent, birthday=date_birthday, last_active=date.today())
    new_child.save()
    userchild = UserChild(parent=parent_id, child=new_child.id)
    userchild.save()
    return JsonResponse({'success':  True, 'message': new_child.register_info()})


def login_user(email, password):
    user = User.objects.filter(email=email, password=password)
    if user:
        return JsonResponse({'success': True, 'message': user[0].login_info()})
    else:
        if User.objects.filter(email=email):
            return JsonResponse({'success':  False, 'message': "Wrong password"}, status=400)
        else:
            return JsonResponse({'success': False, 'message': "No such user"}, status=550)


def refactor_str(st, str_to_replace):
    substring = st[st.find("{") + 1:st.rfind("}")]
    st = st.replace(substring, str_to_replace)
    final_st = "".join([char for char in st if char != "{" and char != "}"])
    return final_st


def get_milestones_by_child(child_id):
    child = Child.objects.get(pk=child_id)
    parent = child.get_parent()
    milestones = Milestone.objects.filter(target_age=child.get_age(), lang=parent.lang)
    return milestones


def add_result(child_id, test_id, value):
    child = Child.objects.get(pk=child_id)
    parent = child.get_parent()
    test = Test.objects.get(pk=test_id)
    milestone = test.get_milestone()
    existing_results = Result.objects.filter(key_child=child_id, key_milestone=milestone.id)
    if existing_results:
        existing_results[0].result_value = value
        existing_results[0].date = date.today()
        existing_results[0].save()
    else:
        result = Result(key_child=child_id, key_milestone=milestone.id,
                        key_user=parent.id, result_value=value, datetime=date.today())
        result.save()
    if value:
        follow_test = Test.objects.filter(pk=test.follow_up_question)
        if follow_test:
            return follow_test[0]
        else:
            return None
    else:
        backwards_test = Test.objects.filter(pk=test.back_question)
        if backwards_test:
            return backwards_test[0]
        else:
            return None


def results_to_string(results):
    if results:
        str_results = ""
        for result in results:
            milestone = result.get_milestone()
            milestone_ex = MilestonesExercises.objects.filter(milestone=milestone.id)
            if not result.result_value and milestone_ex:
                exercise_desc = str(Exercise.objects.get(pk=milestone_ex[0].exercise))
            else:
                exercise_desc = ""
            str_results = str_results + str(result) + exercise_desc + "\n"
    else:
        str_results = "No results yet"
    return str_results


def get_all_results(parent_id):
    parent = User.objects.get(pk=parent_id)
    children = parent.get_children()
    if children:
        str_children = ""
        for child in children:
            str_children = str_children + child.first_name + " : "
            results = Result.objects.filter(key_child=child.id)
            str_children = str_children + "\n" + results_to_string(results) + "\n"
        return {'message': str_children}
    else:
        return {'message': "No results yet"}


def start_conversation(child_id):
    child = Child.objects.get(pk=child_id)
    child.lastActive = date.today()
    child.save()
    results = child.get_results()
    false_results = child.get_value_results(False)
    failed = ""
    if results:
        if false_results:
            failed = "Let's repeat the failed tests."
            return {'message1': "Hello! " + child.first_name +
                                "'s results from the last time are below.\n "
                                + results_to_string(results) + "\n" + failed,
                    'message2': false_results[0].get_milestone().get_test().description,
                    'test_id': false_results[0].get_milestone().get_test().id}
        else:
            milestone = get_next_milestone(child_id)
            if milestone:
                test = milestone.get_test()
                return {'message1': "Hello! " + child.first_name +
                                    "'s results from the last time are below.\n "
                                    + results_to_string(results) + "\n" + failed,
                        'message2': test.description,
                        'test_id': test.id}
            else:
                return {'message1': "Hello! " + child.first_name +
                                    "'s results from the last time are below.\n "
                                    + results_to_string(results) + "\n" + failed,
                        'message2': "There are no more questions"}

    else:
        milestones = get_milestones_by_child(child_id)
        if milestones:
            for i in range(len(milestones)):
                test = milestones[i].get_test()
                if test is not None:
                    return {'message1': "Hello! Let's start evaluating "+child.first_name,
                            'message2': refactor_str(test.description, child.first_name),
                            'test_id': test.id}
            return {'message': "There are no check-ups for the age of " + str(child.get_age())}
        else:
            return {'message': "There are no check-ups for the age of " + str(child.get_age())}


def get_next_milestone(child_id):
    milestones = get_milestones_by_child(child_id)
    for milestone in milestones:
        result = Result.objects.filter(key_child=child_id,
                                       key_milestone=milestone.id, result_value=False)
        if result and result[0].datetime != date.today():
            return milestone
    return None


def process_milestone(milestone, child_id):
    if milestone:
        test = milestone.get_test()
        return {'message': test.description, 'test_id': test.id}
    else:
        return {'message': "Evaluation is finished. Here are your child's results. "
                           + results_to_string(Child.objects.get(pk=child_id).get_results())}


def process_message(test_id, child_id, text):
    if text == "Yes":
        value = True
    else:
        value = False
    next_test = add_result(child_id, test_id, value)
    if next_test is None:
        return process_milestone(get_next_milestone(child_id), child_id)
    else:
        milestone = next_test.get_milestone()
        result = Result.objects.filter(key_milestone=milestone[0].id, key_child=child_id)
        if result and result[0].result_value:
            return process_milestone(get_next_milestone(child_id), child_id)
        else:
            return {'message': next_test.description, 'test_id': next_test.id}
