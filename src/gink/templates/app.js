const APIs = {
  path: "/api/v1/path",
  node: "/api/v1/node",
}

const GetActionPath = () => {
  return axios.get(APIs.path)
}

const SaveActionPath = (payload) => {
  return axios.post(APIs.path, payload)
}

const SaveNode = (payload) => {
  return axios.post(APIs.node, payload)
}


ELEMENT.locale(ELEMENT.lang.en)

new Vue({
  el: '#app',
  data: () => {
    return {
      activeTab: 0,
      currentNode: null,
      nodes: null,
      manualDescription: '',
      dialogFormVisible: false,
      startDialogFormVisible: true,
      person: {
        email: null,
        lmu: null,
        age: null,
        gender: null,
      }
    }
  },
  created: function() {
    this.GetActionPath()
    this.currentNode = this.nodes[0]
  },
  methods: {
    GetActionPath() {
      const self = this
      GetActionPath().then((response) => {
        if (response.status === 200) {
          self.nodes = response.data.nodes
          if (self.nodes) {
            self.currentNode = self.nodes[self.activeTab]
          }
          return Promise.resolve(response.data.nodes)
        }
        self.$message.error("Get Action Path failed, please try again")
        return Promise.reject(response.status)
      })
    },
    saveActionPath() {
      const self = this

      if (self.manualDescription.length < 20) {
        self.$message.error("Your description is too short, please describe more :(")
        return
      }

      urls = []
      for (i = 0; i < self.nodes.length; i++) {
        urls.push(self.nodes[i].url)
      }
      console.log("age: ", self.person.age)
      self.person.age = parseInt(self.person.age, 10)
      console.log("age: ", self.person.age)
      if (!Number.isInteger(self.person.age)) {
        self.person.age = 0
      }
      SaveActionPath({
        email: self.person.email,
        lmu: self.person.lmu,
        age: self.person.age,
        gender: self.person.gender,
        path: urls,
        manual_desc: self.manualDescription
      }).then((response) => {
        console.log(response)
        self.$message.success(response.data.message + " Your task has been updated.")
        self.GetActionPath()
        self.manualDescription = ''
      })
    },
    changeActionPath() {
      const self = this
      self.$message.success("Your task has been updated.")
      self.GetActionPath()
      self.manualDescription = ''
    },
    editCurrentNode() {
      this.dialogFormVisible = true
    },
    saveInfo() {
      if (this.person.email === null &&
          this.person.lmu === null && 
          this.person.age === null && 
          this.person.gender === null) {
        this.$message.success("Thank you very much :)")
        this.startDialogFormVisible = false
        return
      }
      this.$message.success("Your informations are saved. Please don't refresh the page during your participation")
      this.startDialogFormVisible = false
    },
    saveCurrentNode() {
      const self = this
      node = JSON.parse(JSON.stringify(self.currentNode))
      node.meta = []
      node.keywords = []
      if (Array.isArray(self.currentNode.meta)) {
        node.meta = [].concat(self.currentNode.meta)
      } else {
        node.meta.push(self.currentNode.meta)
      }

      if (Array.isArray(self.currentNode.keywords)) {
        node.keywords = [].concat(self.currentNode.keywords)
      } else {
        node.keywords.push(self.currentNode.keywords)
      }
      SaveNode(node).then((response) => {
        if (response.status === 200) {
          self.$message.success("Editing success, thank you very much :)")
          self.dialogFormVisible = false
          return Promise.resolve(response)
        }
        return Promise.reject(response)
      }).catch((error) => {
        console.log(error)
        self.$message.error("Something went wrong, you cannot edit it.")
      })
    },
    tabName(index) {
      return `${index}`
    },
    tabIndex(index) {
      if (index === 0) {
        return 'Starting'
      }
      return 'Step ' + index
    },
    filterSourceCode(source) {
      return source
      // .replace(/(\/\*[\w\'\s\r\n\*]*\*\/)|(\/\/[\w\s\']*)|(\<![\-\-\s\w\>\/]*\>)/g, '')
      // .replace(/\/\*[\s\S]*?\*\//g, '')
      .replace(/\/\*[\s\S]*?\*\/|([^\\:]|^)\/\/.*$/gm, '$1')
      .replace(/(^[ \t]*\n)/gm, '')
      .replace(/<!--[\s\S]*?-->/g, '')
    },
    tabClickHandler(tab) {
      this.activeTab = tab.index
      this.currentNode = this.nodes[parseInt(tab.index, 10)]
    },
  }
})