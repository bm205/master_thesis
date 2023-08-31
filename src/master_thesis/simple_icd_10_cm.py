import xml.etree.ElementTree as ET
import importlib.resources as pkg_resources

import master_thesis.taxonomies as taxonomies


class _CodeTree:
    def __init__(self, tree, all_confirmed_codes, code_to_node, parent = None, seven_chr_def_ancestor = None, 
                    seven_chr_note_ancestor = None, use_additional_code_ancestor = None, code_first_ancestor = None):
        #initialize all the values
        self.name = ""
        self.description = ""
        self.type = ""
        self.parent = parent
        self.children = []
        self.excludes1 = []
        self.excludes2 = []
        self.includes = []
        self.inclusion_term = []
        self.seven_chr_def = {}
        self.seven_chr_def_ancestor = seven_chr_def_ancestor
        self.seven_chr_note = ""
        self.seven_chr_note_ancestor = seven_chr_note_ancestor
        self.use_additional_code = ""
        self.use_additional_code_ancestor = use_additional_code_ancestor
        self.code_first = ""
        self.code_first_ancestor = code_first_ancestor
        
        #reads the data from the subtrees
        new_seven_chr_def_ancestor=seven_chr_def_ancestor
        new_seven_chr_note_ancestor=seven_chr_note_ancestor
        new_use_additional_code_ancestor=use_additional_code_ancestor
        new_code_first_ancestor=code_first_ancestor
        if "id" in tree.attrib: #the name of sections is an attribute instead of text inside an XML element
            self.name=tree.attrib["id"]
        for subtree in tree:
            if subtree.tag=="section" or subtree.tag=="diag": #creates a new child for this node
                self.children.append(
                    _CodeTree(
                    subtree,
                    all_confirmed_codes,
                    code_to_node,
                    parent=self,
                    seven_chr_def_ancestor=new_seven_chr_def_ancestor,
                    seven_chr_note_ancestor=new_seven_chr_note_ancestor,
                    use_additional_code_ancestor=new_use_additional_code_ancestor,
                    code_first_ancestor=new_code_first_ancestor)
                    )
            elif subtree.tag=="name":
                self.name=subtree.text
            elif subtree.tag=="desc":
                self.description=subtree.text
            elif subtree.tag=="excludes1":
                for note in subtree:
                    self.excludes1.append(note.text)
            elif subtree.tag=="excludes2":
                for note in subtree:
                    self.excludes2.append(note.text)
            elif subtree.tag=="includes":
                for note in subtree:
                    self.includes.append(note.text)
            elif subtree.tag=="inclusionTerm":
                for note in subtree:
                    self.inclusion_term.append(note.text)
            elif subtree.tag=="sevenChrDef":
                last_char = None
                for extension in subtree:
                    if extension.tag=="extension":
                        self.seven_chr_def[extension.attrib["char"]]=extension.text
                        last_char = extension.attrib["char"]
                    elif extension.tag=="note":
                        self.seven_chr_def[last_char]=self.seven_chr_def[last_char]+"/"+extension.text
                new_seven_chr_def_ancestor=self
            elif subtree.tag=="sevenChrNote":
                self.seven_chr_note=subtree[0].text
                new_seven_chr_note_ancestor=self
            elif subtree.tag=="useAdditionalCode":
                for i in range(0,len(subtree)):#in case there are multiple lines
                    self.use_additional_code=self.use_additional_code+"\n"+subtree[i].text
                new_use_additional_code_ancestor=self
            elif subtree.tag=="codeFirst":
                for i in range(0,len(subtree)):#in case there are multiple lines
                    self.code_first=self.code_first+"\n"+subtree[i].text
                new_code_first_ancestor=self
        
        #cleans the use_additional_code and code_first fields from extra new lines
        if self.use_additional_code!="" and self.use_additional_code[0]=="\n":
            self.use_additional_code=self.use_additional_code[1:]
        if self.code_first!="" and self.code_first[0]=="\n":
            self.code_first=self.code_first[1:]
        
        #sets the type
        if tree.tag=="chapter":
            self.type="chapter"
        elif tree.tag=="section":
            self.type="section"
        elif tree.tag=="diag_ext":
            self.type="extended subcategory"
        elif tree.tag=="diag" and len(self.name)==3:
            self.type="category"
        else:
            self.type="subcategory"
        
        #adds the new node to the dictionary
        if self.name not in code_to_node:#in case a section has the same name of a code (ex B99)
            code_to_node[self.name]=self
        
        #if this code is a leaf, it adds to its children the codes created by adding the seventh character
        if len(self.children)==0 and (self.seven_chr_def!={} or self.seven_chr_def_ancestor!=None) and self.type!="extended subcategory":
            if self.seven_chr_def!={}:
                dictionary = self.seven_chr_def
            else:
                dictionary = self.seven_chr_def_ancestor.seven_chr_def
            extended_name=self.name
            if len(extended_name)==3:
                extended_name=extended_name+"."
            while len(extended_name)<7:#adds the placeholder X if needed
                extended_name = extended_name+"X"
            for extension in dictionary:
                if((extended_name[:3]+extended_name[4:]+extension) in all_confirmed_codes):
                    #checks if there's a special rule that excludes this new code
                    new_XML = "<diag_ext><name>"+extended_name+extension+"</name><desc>"+self.description+", "+dictionary[extension]+"</desc></diag_ext>"
                    self.children.append(
                        _CodeTree(
                        ET.fromstring(new_XML),
                        all_confirmed_codes,
                        code_to_node,
                        parent=self,
                        seven_chr_def_ancestor=new_seven_chr_def_ancestor,
                        seven_chr_note_ancestor=new_seven_chr_note_ancestor,
                        use_additional_code_ancestor=new_use_additional_code_ancestor,
                        code_first_ancestor=new_code_first_ancestor)
                        )


class SimpleIcd10Cm:
    def __init__(self) -> None:
        self.chapter_list: list["_CodeTree"] = []
        self.code_to_node: dict[str, "_CodeTree"] = {}
        self.all_codes_list: list[str] = []
        self.all_codes_list_no_dots: list[str] = []
        self.code_to_index_dictionary: dict[str, int] = {}

        self._load_codes()

    def _load_codes(self,):
        #loads the list of all codes, to remove later from the tree the ones that do not exist for very specific rules not easily extracted from the XML file
        f = pkg_resources.read_text(taxonomies, 'icd10cm-order-Jan-2021.txt')
        
        all_confirmed_codes = set()
        lines=f.split("\n")
        for line in lines:
            all_confirmed_codes.add(line[6:13].strip())
        
        #creates the tree
        root = ET.fromstring(pkg_resources.read_text(taxonomies, 'icd10cm_tabular_2021.xml'))
        root.remove(root[0])
        root.remove(root[0])
        for child in root:
            self.chapter_list.append(_CodeTree(child, all_confirmed_codes, self.code_to_node))

    def _add_dot_to_code(self, code):
        if len(code)<4 or code[3]==".":
            return code
        elif code[:3]+"."+code[3:] in self.code_to_node:
            return code[:3]+"."+code[3:]
        else:
            return code

    def is_valid_item(self, code: str) -> bool:
        return code in self.code_to_node or len(code)>=4 and code[:3]+"."+code[3:] in self.code_to_node

    def is_chapter(self, code: str) -> bool:
        code = self._add_dot_to_code(code)
        if code in self.code_to_node:
            return self.code_to_node[code].type=="chapter"
        else:
            return False

    def is_block(self, code: str) -> bool:
        code = self._add_dot_to_code(code)
        if code in self.code_to_node:
            return self.code_to_node[code].type=="section" or self.code_to_node[code].parent!=None and self.code_to_node[code].parent.name==code #second half of the or is for sections containing a single category
        else:
            return False

    def is_category(self, code: str) -> bool:
        code = self._add_dot_to_code(code)
        if code in self.code_to_node:
            return self.code_to_node[code].type=="category"
        else:
            return False

    def is_subcategory(self, code: str, include_extended_subcategories=True) -> bool:
        code = self._add_dot_to_code(code)
        if code in self.code_to_node:
            return self.code_to_node[code].type=="subcategory" or self.code_to_node[code].type=="extended subcategory" and include_extended_subcategories
        else:
            return False

    def is_extended_subcategory(self, code: str) -> bool:
        code = self._add_dot_to_code(code)
        if code in self.code_to_node:
            return self.code_to_node[code].type=="extended subcategory"
        else:
            return False
        
    def is_category_or_subcategory(self, code: str) -> bool:
        return self.is_subcategory(code) or self.is_category(code)

    def is_chapter_or_block(self, code: str) -> bool:
        return self.is_block(code) or self.is_chapter(code)

    def get_description(self, code: str, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            return node.parent.description
        else:
            return node.description

    def get_excludes1(self, code: str, prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            return node.parent.excludes1.copy()
        else:
            return node.excludes1.copy()

    def get_excludes2(self, code: str, prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            return node.parent.excludes2.copy()
        else:
            return node.excludes2.copy()

    def get_includes(self, code: str, prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            return node.parent.includes.copy()
        else:
            return node.includes.copy()

    def get_inclusion_term(self, code: str, prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            return node.parent.inclusion_term.copy()
        else:
            return node.inclusion_term.copy()

    def get_seven_chr_def(self, code: str, search_in_ancestors=False, prioritize_blocks=False) -> dict[str, str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        res = node.seven_chr_def.copy()
        if search_in_ancestors and len(res)==0 and node.seven_chr_def_ancestor!=None:
            return node.seven_chr_def_ancestor.seven_chr_def.copy()
        else:
            return res

    def get_seven_chr_note(self, code: str, search_in_ancestors=False, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        res = node.seven_chr_note
        if search_in_ancestors and res=="" and node.seven_chr_note_ancestor!=None:
            return node.seven_chr_note_ancestor.seven_chr_note
        else:
            return res

    def get_use_additional_code(self, code: str, search_in_ancestors=False, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        res = node.use_additional_code
        if search_in_ancestors and res=="" and node.use_additional_code_ancestor!=None:
            return node.use_additional_code_ancestor.use_additional_code
        else:
            return res

    def get_code_first(self, code: str, search_in_ancestors=False, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        res = node.code_first
        if search_in_ancestors and res=="" and node.code_first_ancestor!=None:
            return node.code_first_ancestor.code_first
        else:
            return res

    def get_parent(self, code: str, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        if node.parent!=None:
            return node.parent.name
        else:
            return ""

    def get_children(self, code: str, prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        res = []
        for child in node.children:
            res.append(child.name)
        return res

    def is_leaf(self, code: str, prioritize_blocks=False) -> bool:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        return len(node.children)==0

    def get_full_data(self, code: str, search_in_ancestors=False, prioritize_blocks=False) -> str:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        str = "Name:\n"+node.name+"\nDescription:\n"+node.description
        if node.parent!=None:
            str = str + "\nParent:\n" + node.parent.name
        if node.excludes1!=[]:
            str = str + "\nexcludes1:"
            for item in node.excludes1:
                str = str + "\n" + item
        if node.excludes2!=[]:
            str = str + "\nexcludes2:"
            for item in node.excludes2:
                str = str + "\n" + item
        if node.includes!=[]:
            str = str + "\nincludes:"
            for item in node.includes:
                str = str + "\n" + item
        if node.inclusion_term!=[]:
            str = str + "\ninclusion term:"
            for item in node.inclusion_term:
                str = str + "\n" + item
        seven_chr_note=self.get_seven_chr_note(code,search_in_ancestors=search_in_ancestors,prioritize_blocks=prioritize_blocks)
        if seven_chr_note!="":
            str = str + "\nseven chr note:\n" + seven_chr_note
        seven_chr_def=self.get_seven_chr_def(code,search_in_ancestors=search_in_ancestors,prioritize_blocks=prioritize_blocks)
        if seven_chr_def!={}:
            str = str + "\nseven chr def:"
            for item in seven_chr_def:
                str = str + "\n" + item + ":\t" + seven_chr_def[item]
        use_additional=self.get_use_additional_code(code,search_in_ancestors=search_in_ancestors,prioritize_blocks=prioritize_blocks)
        if use_additional!="":
            str = str + "\nuse additional code:\n" + use_additional
        code_first=self.get_code_first(code,search_in_ancestors=search_in_ancestors,prioritize_blocks=prioritize_blocks)
        if code_first!="":
            str = str + "\ncode first:\n" + code_first
        if node.children==[]:
            str = str + "\nChildren:\nNone--"
        else:
            str = str + "\nChildren:\n"
            for child in node.children:
                str = str + child.name + ", "
        return str[:-2]

    def get_ancestors(self, code: str,prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        result = []
        while node.parent != None:
            result.append(node.parent.name)
            node=node.parent
        return result

    def get_descendants(self, code: str,prioritize_blocks=False) -> list[str]:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(code)]
        if prioritize_blocks and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        result = []
        self._add_children_to_list(node, result)
        return result

    def _add_children_to_list(self, node, list):
        for child in node.children:
            list.append(child.name)
            self._add_children_to_list(child,list)

    def is_ancestor(self, a:str,b:str,prioritize_blocks_a=False,prioritize_blocks_b=False) -> bool:
        if not self.is_valid_item(a):
            raise ValueError("The code \""+a+"\" does not exist.")
        node = self.code_to_node[self._add_dot_to_code(a)]
        if prioritize_blocks_a and node.parent!=None and node.parent.name==node.name:
            node = node.parent
        return a in self.get_ancestors(b, prioritize_blocks=prioritize_blocks_b) and (a!=b or prioritize_blocks_a)

    def is_descendant(self, a:str,b:str,prioritize_blocks_a=False,prioritize_blocks_b=False) -> bool:
        return self.is_ancestor(b,a,prioritize_blocks_a=prioritize_blocks_b,prioritize_blocks_b=prioritize_blocks_a)

    def get_nearest_common_ancestor(self, a:str,b:str,prioritize_blocks_a=False,prioritize_blocks_b=False) -> str:
        anc_a = [self._add_dot_to_code(a)] + self.get_ancestors(a, prioritize_blocks=prioritize_blocks_a)
        anc_b = [self._add_dot_to_code(b)] + self.get_ancestors(b, prioritize_blocks=prioritize_blocks_b)
        if len(anc_b) > len(anc_a):
            temp = anc_a
            anc_a = anc_b
            anc_b = temp
        for anc in anc_a:
            if anc in anc_b:
                return anc
        return ""

    def get_all_codes(self, with_dots=True) -> list[str]:
        if self.all_codes_list==[]:
            for chapter in self.chapter_list:
                self._add_tree_to_list(chapter)
        if with_dots:
            return self.all_codes_list.copy()
        else:
            return self.all_codes_list_no_dots.copy()

    def _add_tree_to_list(self, tree):
        self.all_codes_list.append(tree.name)
        if(len(tree.name)>4 and tree.name[3]=="."):
            self.all_codes_list_no_dots.append(tree.name[:3]+tree.name[4:])
        else:
            self.all_codes_list_no_dots.append(tree.name)
        for child in tree.children:
            self._add_tree_to_list(child)

    def get_index(self, code: str) -> int:
        if not self.is_valid_item(code):
            raise ValueError("The code \""+code+"\" does not exist.")
        code = self._add_dot_to_code(code)
        if self.all_codes_list==[]:
            for chapter in self.chapter_list:
                self._add_tree_to_list(chapter)
        if code in self.code_to_index_dictionary:
            return self.code_to_index_dictionary[code]
        else:
            i=0
            for c in self.all_codes_list:
                if c==code:
                    self.code_to_index_dictionary[code]=i
                    return i
                else:
                    i=i+1

    def remove_dot(self, code: str) -> str:
        if self.all_codes_list==[]:
            for chapter in self.chapter_list:
                self._add_tree_to_list(chapter)
        return self.all_codes_list_no_dots[self.get_index(code)]

    def add_dot(self, code: str) -> str:
        if self.all_codes_list==[]:
            for chapter in self.chapter_list:
                self._add_tree_to_list(chapter)
        return self.all_codes_list[self.get_index(code)]


if __name__ == "__main__":
    cm = SimpleIcd10Cm()
    print(cm.get_children("A01"))