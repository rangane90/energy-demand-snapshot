import hudson.plugins.git.BranchSpec
import hudson.plugins.git.GitSCM
import hudson.plugins.git.UserRemoteConfig
import jenkins.model.Jenkins
import org.jenkinsci.plugins.workflow.cps.CpsScmFlowDefinition
import org.jenkinsci.plugins.workflow.job.WorkflowJob

// Use the disposable runner as the only executor. Jenkins listens on loopback.
def jenkins = Jenkins.get()
jenkins.setNumExecutors(1)
jenkins.setLabelString('docker')

def repository = System.getenv('GITHUB_REPOSITORY')
def revision = System.getenv('GITHUB_SHA')
def remote = new UserRemoteConfig("https://github.com/${repository}.git".toString(), null, null, null)
def scm = new GitSCM([remote], [new BranchSpec(revision)], null, null, [])
def job = jenkins.createProject(WorkflowJob, 'energy-demand-snapshot')
job.setDefinition(new CpsScmFlowDefinition(scm, 'Jenkinsfile'))
job.save()

if (job.scheduleBuild2(0) == null) {
    throw new IllegalStateException('Could not queue the Jenkins verification job')
}
