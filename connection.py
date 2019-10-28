class Connection:
    def __init__(self, id):
        self.id = id
        self.uid = -1
        self.username = ""
        self.inode = -1
        self.program = ""
        self.src = {"hostname":"", "ip":"", "port":""}
        self.dest = {"hostname":"", "ip":"", "port":""}

    def updateUid(self, uid):
        self.uid = uid

    def updateUsername(self, username):
        self.username = username

    def updateInode(self, inode):
        self.inode = inode

    def updateProgram(self, program):
        self.program = program

    def updateSrc(self, src):
        self.src = src

    def updateDest(self, dest):
        self.dest = dest

    def updateAll(self, uid, username, inode,program,src,dest):
        self.updateUid(uid)
        self.updateUsername(username)
        self.updateInode(inode)
        self.updateProgram(program)
        self.updateSrc(src)
        self.updateDest(dest)

    def __eq__(self, other): 
        if not isinstance(other, Connection):
            return NotImplemented

        return self.id == other.id

    def __str__(self):


        msg = "\nID:\t{}\n UserName\t{}\tUID:\t{}\n Program:\t{}\tInode:\t{}\n Src:\t{}\n Dest:\t{}\n".format(
            self.id,
            self.username,
            self.uid,
            self.program,
            self.inode,
            self.src,
            self.dest
        )

        return msg

    def __repr__(self):
        return str(self)