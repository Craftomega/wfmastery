# pylint: disable-msg=C0103,C0301,C0111,E1101,C0321
#kindly fuck off, I know

import data_v1 as d1
import operator as OP

item_element = """
            <label class="individual" id="{id}" data-id="{id}" data-state="False">{name}</label>
            <input class="individual_input" name="{id}" type="checkbox" data-category="{category}" data-subcategory="{subcategory}" data-id="{id}" value=0>
"""

# item_line = """<span class="subgroup_box">
#                     <label class="subgroup">{name}</label>
#                     <span class="sgroup_box">{body}</span>
#                </span><br/>
# """

item_line = """{body}"""

main_group = """
    <fieldset class="menu_tab" id="category_{category_name}" data-active="{is_on}">
        <legend>{category_name}</legend>
        <span class="type_box">{body}</span>
    </fieldset>
"""
menu_item = """
            <li class="menu-option" id="menutab_{name}" data-active="{is_on}" data-dest="category_{name}">{name}</li>
"""


grocery_item = """
    <li
        class="grocery_item"
        id="grocery_{id}"
        data-active="{is_on}"
        data-state="False"
        data-cat="{category}">{category} -
            <a
                href="http://warframe.wikia.com/wiki/{name}"
                target="_blank"
                >{name}</a>
        </li>

"""

html_body = """
<!doctype html>
<html>
    <head>
        <title>MR hell - Remember this so you can find it in history search</title>
        <link rel="stylesheet" type="text/css" href="./style.css">
        <script src="./script.js"></script>
    </head>
    <body>
        <ul class="menu">
            {menu_names}
        </ul>
        <p>MR hell checklist</p>
        {body}

        <h1>Grocery list</h1>
        <ul id="groceries">
            {grocery_body}
        </ul>
    </body>
    <script>
        var wfmastery = {{}};
        wfmastery.positions = {pos_data};
        wfmastery.json_id2pos = {json_id2pos};
    </script>
</html>
"""


def main():


    group_html = ""
    grocery_buffer = ""

    sorted_main_types = "Primary,Secondary,Melee,Sentinel,Dojo,Archwing".split(",")
    active_type = "Primary"

    for group_key in sorted_main_types:
        temp = d1.indexed[group_key]

        all_things = []
        for sub_type in temp.values():
            all_things.extend(sub_type)
        all_things = sorted(all_things, key=lambda x: x['name'])
        sub_buffer = ""
        for thing in all_things:
            item_html = item_element.format(**thing)
            sub_buffer += item_html

            grocery_buffer += grocery_item.format(
                category=d1.category[thing["category"]],
                name=thing["name"],
                is_on=d1.category[thing["category"]] == active_type,
                id=thing['id']
            )


        group_html += main_group.format(category_name=group_key, body=sub_buffer, is_on=group_key == active_type)

        # for subcategory in sorted(temp.keys()):
        #     sub_buffer = ""
        #     ordered = sorted(temp[subcategory], key=lambda x: x["name"])
        #
        #     for thing in ordered:
        #         item_html = item_element.format(**thing)
        #         sub_buffer += item_html + "\n"
        #     buffer += item_line.format(name=subcategory, body=sub_buffer) + "\n"

        # group_html += main_group.format(category_name=group_key, body=buffer, is_on=group_key == active_type)


    menu_list = "\n".join([menu_item.format(name=x, is_on=sorted_main_types[0] == x) for x in sorted_main_types])

    #Build grocery list

    json_positions = json.dumps(d1.positions, indent=4, sort_keys=True)
    json_id2pos = json.dumps(d1.id2position, indent=4, sort_keys=True)


    with open("index.html", "w") as my_file:
        my_file.write(
            html_body.format(
                body=group_html,
                menu_names=menu_list,
                grocery_body=grocery_buffer,
                pos_data=json_positions,
                json_id2pos=json_id2pos
            )
        )



if __name__ == '__main__': main()
