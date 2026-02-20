<h1>Secure 3-Tier AWS Architecture (Terraform + FastAPI)</h1>
<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/eb743f19-3b24-4e45-a041-ad7d22cffed2" />
<h2>🚨 Problem</h2>
<p>
Many small deployments expose EC2 instances and databases directly to the internet, rely on manual provisioning, and use SSH-based access. This often leads to:
</p>
<ul>
  <li>Public database exposure</li>
  <li>SSH key sprawl and unmanaged access</li>
  <li>Configuration drift from manual setup</li>
  <li>Limited scalability</li>
  <li>Difficult troubleshooting due to poor network segmentation</li>
</ul>
<p>
Production systems require secure network isolation, controlled access paths, reproducible infrastructure, and observable traffic flow.
</p>

<h2>🛠 Solution</h2>
<p>This project implements a production-style 3-tier AWS architecture designed using cloud best practices to address those risks.</p>

<h3>Design Goals</h3>
<ul>
  <li>Enforce network isolation between tiers</li>
  <li>Eliminate public access to backend and database layers</li>
  <li>Replace SSH access with IAM-based secure access</li>
  <li>Enable reproducible infrastructure using Terraform</li>
  <li>Validate connectivity through structured troubleshooting</li>
</ul>

<h2>🏗 Architecture Overview</h2>

<pre>
Client
   |
   v
[Application Load Balancer - Public Subnets]
   |
   v
[EC2 + FastAPI - Private Subnet]
   |
   v
[RDS PostgreSQL - Private Subnets]
</pre>

<h3>Architecture Highlights</h3>
<ul>
  <li>ALB in public subnets handles inbound HTTP traffic and health checks</li>
  <li>EC2 instance deployed in a private subnet (no public IP)</li>
  <li>RDS PostgreSQL deployed in private subnets with no public endpoint</li>
  <li>Security group–to–security group rules enforce least-privilege communication</li>
  <li>NAT Gateway enables controlled outbound internet access</li>
  <li>AWS Systems Manager (SSM) provides secure, keyless instance access</li>
</ul>

<h2>🔐 Security & Access Design</h2>
<ul>
  <li>No public SSH access</li>
  <li>No public database endpoint</li>
  <li>IAM role–based instance permissions</li>
  <li>Layered subnet segmentation</li>
  <li>Controlled ingress and egress rules</li>
</ul>

<h2>⚙️ Infrastructure as Code</h2>
<p>
All infrastructure is provisioned using Terraform, enabling:
</p>
<ul>
  <li>Reproducible environments</li>
  <li>Consistent configuration across deployments</li>
  <li>Reduced configuration drift</li>
  <li>Version-controlled infrastructure changes</li>
</ul>

<h2>🔧 Operational Validation & Troubleshooting</h2>
<ul>
  <li>Verified ALB health check behavior</li>
  <li>Troubleshot security group misconfigurations</li>
  <li>Validated NAT Gateway outbound routing</li>
  <li>Confirmed private EC2-to-RDS connectivity</li>
  <li>Tested end-to-end request flow from client to database</li>
</ul>

<h2>⚙️ Application Layer</h2>
<ul>
  <li>FastAPI backend deployed on EC2</li>
  <li>PostgreSQL database hosted on Amazon RDS</li>
  <li>Health check endpoint exposed for ALB monitoring</li>
  <li>Database connectivity restricted to private networking</li>
</ul>

<h3>API Endpoints</h3>
<ul>
  <li><code>GET /</code> → Health check</li>
  <li><code>POST /todos</code> → Create a new todo</li>
  <li><code>GET /todos</code> → List all todos</li>
</ul>

<h2>🚀 Future Improvements</h2>
<ul>
  <li>Auto Scaling Group for EC2 instances</li>
  <li>HTTPS termination with ACM</li>
  <li>CI/CD pipeline integration</li>
  <li>CloudWatch monitoring and alarms</li>
  <li>Blue/green deployment strategy</li>
</ul>

<h2>📈 Why This Project Matters</h2>
<ul>
  <li>Cloud architecture design principles</li>
  <li>Secure infrastructure patterns</li>
  <li>Infrastructure automation using Terraform</li>
  <li>Operational debugging and connectivity validation</li>
  <li>Production-style thinking rather than tutorial deployment</li>
</ul>





<img width="1369" height="234" alt="Screenshot from 2026-01-27 22-12-43" src="https://github.com/user-attachments/assets/946fe388-548c-408a-a692-cf6003041c02" />

<img width="915" height="490" alt="Screenshot from 2026-01-28 00-05-26" src="https://github.com/user-attachments/assets/2a16ae46-0846-48a8-8bbd-088c58708dbb" />

---



