# 工作报告

> **日期:** 2026-05-16
> **作者:** IVEN-CN

---

## 仓库: `E:\code\code_project\bluenet_web2.2\develop`

### `c1c1c183` chore: 归档 assessment-team-support OpenSpec 变更

- **时间:** 2026-05-16 22:43:16 +0800

**提交信息:**

chore: 归档 assessment-team-support OpenSpec 变更

**代码变更:**

```diff
diff --git a/openspec/changes/assessment-team-support/.openspec.yaml b/openspec/changes/archive/2026-05-16-assessment-team-support/.openspec.yaml
similarity index 100%
rename from openspec/changes/assessment-team-support/.openspec.yaml
rename to openspec/changes/archive/2026-05-16-assessment-team-support/.openspec.yaml
diff --git a/openspec/changes/assessment-team-support/design.md b/openspec/changes/archive/2026-05-16-assessment-team-support/design.md
similarity index 100%
rename from openspec/changes/assessment-team-support/design.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/design.md
diff --git a/openspec/changes/assessment-team-support/proposal.md b/openspec/changes/archive/2026-05-16-assessment-team-support/proposal.md
similarity index 100%
rename from openspec/changes/assessment-team-support/proposal.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/proposal.md
diff --git a/openspec/changes/assessment-team-support/specs/assessment-judgement/spec.md b/openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-judgement/spec.md
similarity index 100%
rename from openspec/changes/assessment-team-support/specs/assessment-judgement/spec.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-judgement/spec.md
diff --git a/openspec/changes/assessment-team-support/specs/assessment-team-support/spec.md b/openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-team-support/spec.md
similarity index 100%
rename from openspec/changes/assessment-team-support/specs/assessment-team-support/spec.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-team-support/spec.md
diff --git a/openspec/changes/assessment-team-support/specs/assessment-time-management/spec.md b/openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-time-management/spec.md
similarity index 100%
rename from openspec/changes/assessment-team-support/specs/assessment-time-management/spec.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/specs/assessment-time-management/spec.md
diff --git a/openspec/changes/assessment-team-support/specs/frontend-assessment-question-page/spec.md b/openspec/changes/archive/2026-05-16-assessment-team-support/specs/frontend-assessment-question-page/spec.md
similarity index 100%
rename from openspec/changes/assessment-team-support/specs/frontend-assessment-question-page/spec.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/specs/frontend-assessment-question-page/spec.md
diff --git a/openspec/changes/assessment-team-support/tasks.md b/openspec/changes/archive/2026-05-16-assessment-team-support/tasks.md
similarity index 100%
rename from openspec/changes/assessment-team-support/tasks.md
rename to openspec/changes/archive/2026-05-16-assessment-team-support/tasks.md
```

### `62a6d96e` test: 新增考核队伍相关单元测试和集成测试，修复现有测试参数不匹配问题

- **时间:** 2026-05-16 22:21:20 +0800

**提交信息:**

test: 新增考核队伍相关单元测试和集成测试，修复现有测试参数不匹配问题

- 新增AssessmentTeamRepositoryImpl单元测试
- 新增AssessmentTeamAppServiceImpl单元测试
- 新增AssessmentTeamController集成测试
- 修复AlgorithmJudgeAppServiceImplTest中createAnswer方法参数不匹配问题

**代码变更:**

```diff
diff --git a/src/backend/src/test/java/com/bluenet/web/api/controller/v1/AssessmentTeamControllerIntegrationTest.java b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/AssessmentTeamControllerIntegrationTest.java
new file mode 100644
index 0000000..91bb47b
--- /dev/null
+++ b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/AssessmentTeamControllerIntegrationTest.java
@@ -0,0 +1,553 @@
+package com.bluenet.web.api.controller.v1;
+
+import com.bluenet.web.BaseIntegrationTest;
+import com.bluenet.web.api.dto.ResponseMessage;
+import com.bluenet.web.api.dto.assessment_team.*;
+import com.bluenet.web.api.dto.auth.StudentIdLoginRequestDTO;
+import com.bluenet.web.api.dto.auth.UserAuthResponseDTO;
+import com.bluenet.web.domain.model.entity.AssessmentTime;
+import com.bluenet.web.domain.model.entity.Role;
+import com.bluenet.web.domain.model.entity.User;
+import com.bluenet.web.domain.model.enumerate.Direction;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTimeDO;
+import com.bluenet.web.infrastructure.repository.dataobject.UserDO;
+import com.bluenet.web.infrastructure.repository.mapper.AssessmentTimeMapper;
+import com.bluenet.web.infrastructure.repository.mapper.RoleMapper;
+import com.bluenet.web.infrastructure.repository.mapper.UserMapper;
+import com.bluenet.web.testcontainers.TestcontainersConfiguration;
+import com.bluenet.web.testsupport.RepositoryTestObjects;
+import org.junit.jupiter.api.BeforeEach;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Test;
+import org.springframework.beans.factory.annotation.Autowired;
+import org.springframework.boot.test.context.SpringBootTest;
+import org.springframework.boot.test.mock.mockito.MockBean;
+import org.springframework.boot.test.web.client.TestRestTemplate;
+import org.springframework.context.annotation.Import;
+import org.springframework.core.ParameterizedTypeReference;
+import org.springframework.http.HttpEntity;
+import org.springframework.http.HttpHeaders;
+import org.springframework.http.HttpMethod;
+import org.springframework.http.HttpStatus;
+import org.springframework.http.ResponseEntity;
+import org.springframework.security.crypto.password.PasswordEncoder;
+import org.springframework.test.context.ActiveProfiles;
+import org.testcontainers.junit.jupiter.Testcontainers;
+
+import java.time.LocalDateTime;
+import java.util.List;
+
+import static org.junit.jupiter.api.Assertions.*;
+
+/**
+ * AssessmentTeamController 集成测试。
+ * <p>
+ * 测试考核队伍相关接口的完整链路。
+ * </p>
+ */
+@DisplayName("AssessmentTeamController 集成测试")
+@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
+@ActiveProfiles("test")
+@Testcontainers
+@Import(TestcontainersConfiguration.class)
+class AssessmentTeamControllerIntegrationTest extends BaseIntegrationTest {
+
+    @Autowired
+    private TestRestTemplate restTemplate;
+
+    @Autowired
+    private UserMapper userMapper;
+
+    @Autowired
+    private RoleMapper roleMapper;
+
+    @Autowired
+    private AssessmentTimeMapper assessmentTimeMapper;
+
+    @Autowired
+    private PasswordEncoder passwordEncoder;
+
+    @MockBean
+    private com.bluenet.web.infrastructure.security.scanner.PermissionScanner permissionScanner;
+
+    private static final String LEADER_STUDENT_ID = "teamleader001";
+    private static final String MEMBER_STUDENT_ID = "teammember001";
+    private static final String TEST_PASSWORD = "testPassword123";
+
+    private Long leaderUserId;
+    private Long memberUserId;
+    private Long assessmentTimeId;
+
+    @BeforeEach
+    void setUpTestData() {
+        // 查找 MEMBER 角色
+        Role memberRole = RepositoryTestObjects.toDomain(roleMapper.selectByName("MEMBER"), Role.class);
+        assertNotNull(memberRole, "MEMBER 角色应存在");
+
+        // 创建队长用户
+        User leaderUser = User.reconstruct(
+                null,
+                LEADER_STUDENT_ID,
+                "leader@test.com",
+                memberRole.getId(),
+                passwordEncoder.encode(TEST_PASSWORD),
+                "队长用户",
+                null,
+                null,
+                null,
+                null,
+                Direction.COMPUTER_VISION,
+                null,
+                null,
+                null,
+                false,
+                null,
+                null,
+                null,
+                null,
+                null);
+        RepositoryTestObjects.insert(userMapper, leaderUser, UserDO.class);
+        leaderUserId = leaderUser.getId();
+
+        // 创建队员用户
+        User memberUser = User.reconstruct(
+                null,
+                MEMBER_STUDENT_ID,
+                "member@test.com",
+                memberRole.getId(),
+                passwordEncoder.encode(TEST_PASSWORD),
+                "队员用户",
+                null,
+                null,
+                null,
+                null,
+                Direction.COMPUTER_VISION,
+                null,
+                null,
+                null,
+                false,
+                null,
+                null,
+                null,
+                null,
+                null);
+        RepositoryTestObjects.insert(userMapper, memberUser, UserDO.class);
+        memberUserId = memberUser.getId();
+
+        // 创建允许组队的考核时间
+        AssessmentTime assessmentTime = AssessmentTime.create(
+                Direction.COMPUTER_VISION,
+                1,
+                2026,
+                LocalDateTime.now().plusDays(1),
+                LocalDateTime.now().plusDays(7),
+                false,
+                null,
+                true);
+        RepositoryTestObjects.insert(assessmentTimeMapper, assessmentTime, AssessmentTimeDO.class);
+        assessmentTimeId = assessmentTime.getId();
+    }
+
+    // ========== 辅助方法 ==========
+
+    private HttpHeaders loginAndGetCookies(String studentId, String password) {
+        StudentIdLoginRequestDTO loginRequest = new StudentIdLoginRequestDTO();
+        loginRequest.setStudentId(studentId);
+        loginRequest.setPassword(password);
+
+        ResponseEntity<ResponseMessage<UserAuthResponseDTO>> loginResponse = restTemplate.exchange(
+                "/api/v1/auth/login/student-id",
+                HttpMethod.POST,
+                new HttpEntity<>(loginRequest),
+                new ParameterizedTypeReference<ResponseMessage<UserAuthResponseDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, loginResponse.getStatusCode());
+        List<String> setCookies = loginResponse.getHeaders().get(HttpHeaders.SET_COOKIE);
+        assertNotNull(setCookies, "登录响应应包含 Set-Cookie");
+
+        StringBuilder cookieBuilder = new StringBuilder();
+        for (String setCookie : setCookies) {
+            int semicolonIndex = setCookie.indexOf(';');
+            String nameValue = semicolonIndex > 0 ? setCookie.substring(0, semicolonIndex) : setCookie;
+            if (cookieBuilder.length() > 0) {
+                cookieBuilder.append("; ");
+            }
+            cookieBuilder.append(nameValue);
+        }
+
+        HttpHeaders headers = new HttpHeaders();
+        headers.set(HttpHeaders.COOKIE, cookieBuilder.toString());
+        String csrfToken = loginResponse.getBody().getData().getCsrfToken();
+        headers.set("X-CSRF-Token-Stored", csrfToken);
+        return headers;
+    }
+
+    private String getStoredCsrfToken(HttpHeaders headers) {
+        return headers.getFirst("X-CSRF-Token-Stored");
+    }
+
+    private HttpHeaders createHeadersWithCsrf(HttpHeaders cookies) {
+        HttpHeaders headers = new HttpHeaders();
+        headers.set(HttpHeaders.COOKIE, cookies.getFirst(HttpHeaders.COOKIE));
+        headers.set("X-CSRF-Token", getStoredCsrfToken(cookies));
+        return headers;
+    }
+
+    // ========== 测试用例 ==========
+
+    @Test
+    @DisplayName("创建队伍：已登录用户应成功创建")
+    void createTeam_authenticated_shouldSucceed() {
+        HttpHeaders cookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders headers = createHeadersWithCsrf(cookies);
+
+        CreateTeamRequestDTO request = new CreateTeamRequestDTO();
+        request.setAssessmentTimeId(assessmentTimeId);
+        request.setName("蓝网先锋队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(request, headers),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<AssessmentTeamDTO> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+
+        AssessmentTeamDTO team = body.getData();
+        assertNotNull(team);
+        assertEquals("蓝网先锋队", team.getName());
+        assertEquals(assessmentTimeId, team.getAssessmentTimeId());
+        assertNotNull(team.getInviteCode());
+        assertEquals(1, team.getMembers().size());
+    }
+
+    @Test
+    @DisplayName("创建队伍：未登录应返回401")
+    void createTeam_unauthenticated_shouldReturn401() {
+        CreateTeamRequestDTO request = new CreateTeamRequestDTO();
+        request.setAssessmentTimeId(assessmentTimeId);
+        request.setName("未登录队伍");
+
+        ResponseEntity<ResponseMessage> response = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(request),
+                ResponseMessage.class);
+
+        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
+    }
+
+    @Test
+    @DisplayName("创建队伍：重复创建应返回400")
+    void createTeam_duplicate_shouldReturn400() {
+        HttpHeaders cookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders headers = createHeadersWithCsrf(cookies);
+
+        // 第一次创建
+        CreateTeamRequestDTO request = new CreateTeamRequestDTO();
+        request.setAssessmentTimeId(assessmentTimeId);
+        request.setName("第一次创建");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> firstResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(request, headers),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, firstResponse.getStatusCode());
+
+        // 第二次创建同一考核
+        request.setName("第二次创建");
+        ResponseEntity<ResponseMessage> secondResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(request, headers),
+                ResponseMessage.class);
+
+        assertEquals(HttpStatus.BAD_REQUEST, secondResponse.getStatusCode());
+    }
+
+    @Test
+    @DisplayName("查询我的队伍：已加入应返回队伍信息")
+    void getMyTeam_hasTeam_shouldReturnTeam() {
+        HttpHeaders cookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders headers = createHeadersWithCsrf(cookies);
+
+        // 先创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("查询测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, headers),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+
+        // 查询我的队伍
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/my-team?assessmentTimeId=" + assessmentTimeId,
+                HttpMethod.GET,
+                new HttpEntity<>(headers),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<AssessmentTeamDTO> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+        assertEquals("查询测试队", body.getData().getName());
+    }
+
+    @Test
+    @DisplayName("查询我的队伍：未加入应返回404")
+    void getMyTeam_noTeam_shouldReturn404() {
+        HttpHeaders cookies = loginAndGetCookies(MEMBER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders headers = createHeadersWithCsrf(cookies);
+
+        ResponseEntity<ResponseMessage> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/my-team?assessmentTimeId=" + assessmentTimeId,
+                HttpMethod.GET,
+                new HttpEntity<>(headers),
+                ResponseMessage.class);
+
+        assertEquals(HttpStatus.NOT_FOUND, response.getStatusCode());
+    }
+
+    @Test
+    @DisplayName("预览队伍：应返回队伍预览信息")
+    void previewTeam_validInviteCode_shouldReturnPreview() {
+        HttpHeaders leaderCookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders leaderHeaders = createHeadersWithCsrf(leaderCookies);
+
+        // 创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("预览测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+        String inviteCode = createResponse.getBody().getData().getInviteCode();
+
+        // 预览队伍
+        PreviewTeamRequestDTO previewRequest = new PreviewTeamRequestDTO();
+        previewRequest.setInviteCode(inviteCode);
+
+        ResponseEntity<ResponseMessage<TeamPreviewResponseDTO>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/preview",
+                HttpMethod.POST,
+                new HttpEntity<>(previewRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<TeamPreviewResponseDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<TeamPreviewResponseDTO> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+        assertEquals("预览测试队", body.getData().getName());
+        assertEquals(1, body.getData().getMemberCount());
+    }
+
+    @Test
+    @DisplayName("加入队伍：队员应成功加入")
+    void joinTeam_valid_shouldSucceed() {
+        HttpHeaders leaderCookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders leaderHeaders = createHeadersWithCsrf(leaderCookies);
+
+        // 队长创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("加入测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+        String inviteCode = createResponse.getBody().getData().getInviteCode();
+
+        // 队员加入队伍
+        HttpHeaders memberCookies = loginAndGetCookies(MEMBER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders memberHeaders = createHeadersWithCsrf(memberCookies);
+
+        JoinTeamRequestDTO joinRequest = new JoinTeamRequestDTO();
+        joinRequest.setInviteCode(inviteCode);
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/join",
+                HttpMethod.POST,
+                new HttpEntity<>(joinRequest, memberHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<AssessmentTeamDTO> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+        assertEquals(2, body.getData().getMembers().size());
+    }
+
+    @Test
+    @DisplayName("离开队伍：队员应成功离开")
+    void leaveTeam_member_shouldSucceed() {
+        HttpHeaders leaderCookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders leaderHeaders = createHeadersWithCsrf(leaderCookies);
+
+        // 队长创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("离开测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+        Long teamId = createResponse.getBody().getData().getId();
+        String inviteCode = createResponse.getBody().getData().getInviteCode();
+
+        // 队员加入
+        HttpHeaders memberCookies = loginAndGetCookies(MEMBER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders memberHeaders = createHeadersWithCsrf(memberCookies);
+
+        JoinTeamRequestDTO joinRequest = new JoinTeamRequestDTO();
+        joinRequest.setInviteCode(inviteCode);
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> joinResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams/join",
+                HttpMethod.POST,
+                new HttpEntity<>(joinRequest, memberHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, joinResponse.getStatusCode());
+
+        // 队员离开
+        LeaveTeamRequestDTO leaveRequest = new LeaveTeamRequestDTO();
+        leaveRequest.setTeamId(teamId);
+
+        ResponseEntity<ResponseMessage<Void>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/leave",
+                HttpMethod.POST,
+                new HttpEntity<>(leaveRequest, memberHeaders),
+                new ParameterizedTypeReference<ResponseMessage<Void>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<Void> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+    }
+
+    @Test
+    @DisplayName("转让队长：队长应成功转让")
+    void transferLeader_leader_shouldSucceed() {
+        HttpHeaders leaderCookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders leaderHeaders = createHeadersWithCsrf(leaderCookies);
+
+        // 队长创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("转让测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+        Long teamId = createResponse.getBody().getData().getId();
+        String inviteCode = createResponse.getBody().getData().getInviteCode();
+
+        // 队员加入
+        HttpHeaders memberCookies = loginAndGetCookies(MEMBER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders memberHeaders = createHeadersWithCsrf(memberCookies);
+
+        JoinTeamRequestDTO joinRequest = new JoinTeamRequestDTO();
+        joinRequest.setInviteCode(inviteCode);
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> joinResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams/join",
+                HttpMethod.POST,
+                new HttpEntity<>(joinRequest, memberHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, joinResponse.getStatusCode());
+
+        // 队长转让
+        TransferLeaderRequestDTO transferRequest = new TransferLeaderRequestDTO();
+        transferRequest.setTeamId(teamId);
+        transferRequest.setNewLeaderId(memberUserId);
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/transfer",
+                HttpMethod.POST,
+                new HttpEntity<>(transferRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<AssessmentTeamDTO> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+        assertEquals(memberUserId, body.getData().getLeaderId());
+    }
+
+    @Test
+    @DisplayName("解散队伍：队长应成功解散")
+    void disbandTeam_leader_shouldSucceed() {
+        HttpHeaders leaderCookies = loginAndGetCookies(LEADER_STUDENT_ID, TEST_PASSWORD);
+        HttpHeaders leaderHeaders = createHeadersWithCsrf(leaderCookies);
+
+        // 队长创建队伍
+        CreateTeamRequestDTO createRequest = new CreateTeamRequestDTO();
+        createRequest.setAssessmentTimeId(assessmentTimeId);
+        createRequest.setName("解散测试队");
+
+        ResponseEntity<ResponseMessage<AssessmentTeamDTO>> createResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams",
+                HttpMethod.POST,
+                new HttpEntity<>(createRequest, leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<AssessmentTeamDTO>>() {
+                });
+        assertEquals(HttpStatus.OK, createResponse.getStatusCode());
+        Long teamId = createResponse.getBody().getData().getId();
+
+        // 队长解散
+        ResponseEntity<ResponseMessage<Void>> response = restTemplate.exchange(
+                "/api/v1/assessment-teams/" + teamId,
+                HttpMethod.DELETE,
+                new HttpEntity<>(leaderHeaders),
+                new ParameterizedTypeReference<ResponseMessage<Void>>() {
+                });
+
+        assertEquals(HttpStatus.OK, response.getStatusCode());
+        ResponseMessage<Void> body = response.getBody();
+        assertNotNull(body);
+        assertEquals(200, body.getCode());
+
+        // 解散后查询应返回404
+        ResponseEntity<ResponseMessage> getResponse = restTemplate.exchange(
+                "/api/v1/assessment-teams/my-team?assessmentTimeId=" + assessmentTimeId,
+                HttpMethod.GET,
+                new HttpEntity<>(leaderHeaders),
+                ResponseMessage.class);
+        assertEquals(HttpStatus.NOT_FOUND, getResponse.getStatusCode());
+    }
+}
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
index 10151ea..9e51e17 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
@@ -323,7 +323,15 @@ class AlgorithmJudgeAppServiceImplTest {
 
     private AssessmentAnswer createAnswer() {
         return AssessmentAnswer
-                .reconstruct(ANSWER_ID, USER_ID, QUESTION_ID, "print(input())", ProgrammingLanguage.PYTHON, null, null);
+                .reconstruct(
+                        ANSWER_ID,
+                        USER_ID,
+                        QUESTION_ID,
+                        "print(input())",
+                        ProgrammingLanguage.PYTHON,
+                        null,
+                        null,
+                        null);
     }
 
     private AlgorithmJudgeJob createJob(JudgeJobStatus status, Long answerId) {
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImplTest.java
new file mode 100644
index 0000000..1db8c71
--- /dev/null
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImplTest.java
@@ -0,0 +1,676 @@
+package com.bluenet.web.application.service.impl;
+
+import com.bluenet.web.application.TeamPreviewResult;
+import com.bluenet.web.application.TeamResult;
+import com.bluenet.web.domain.exception.BadRequest;
+import com.bluenet.web.domain.exception.DataNotFound;
+import com.bluenet.web.domain.exception.Forbidden;
+import com.bluenet.web.domain.model.entity.AssessmentAnswer;
+import com.bluenet.web.domain.model.entity.AssessmentQuestion;
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+import com.bluenet.web.domain.model.entity.AssessmentTime;
+import com.bluenet.web.domain.model.enumerate.Direction;
+import com.bluenet.web.domain.model.enumerate.QuestionType;
+import com.bluenet.web.domain.model.vo.UserVO;
+import com.bluenet.web.domain.repository.AssessmentAnswerRepository;
+import com.bluenet.web.domain.repository.AssessmentQuestionRepository;
+import com.bluenet.web.domain.repository.AssessmentTeamRepository;
+import com.bluenet.web.domain.repository.AssessmentTimeRepository;
+import com.bluenet.web.domain.service.UserDomainService;
+import com.bluenet.web.infrastructure.security.util.UserCTX;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Nested;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.api.extension.ExtendWith;
+import org.mockito.InjectMocks;
+import org.mockito.Mock;
+import org.mockito.MockedStatic;
+import org.mockito.junit.jupiter.MockitoExtension;
+import org.springframework.data.domain.PageImpl;
+
+import java.time.LocalDateTime;
+import java.util.Collections;
+import java.util.List;
+import java.util.Optional;
+
+import static org.junit.jupiter.api.Assertions.*;
+import static org.mockito.ArgumentMatchers.*;
+import static org.mockito.Mockito.*;
+
+@DisplayName("AssessmentTeamAppServiceImpl 单元测试")
+@ExtendWith(MockitoExtension.class)
+class AssessmentTeamAppServiceImplTest {
+
+    @Mock
+    private AssessmentTeamRepository assessmentTeamRepository;
+
+    @Mock
+    private AssessmentTimeRepository assessmentTimeRepository;
+
+    @Mock
+    private AssessmentAnswerRepository assessmentAnswerRepository;
+
+    @Mock
+    private AssessmentQuestionRepository assessmentQuestionRepository;
+
+    @Mock
+    private UserDomainService userDomainService;
+
+    @InjectMocks
+    private AssessmentTeamAppServiceImpl assessmentTeamAppService;
+
+    private static final Long TEST_USER_ID = 1L;
+    private static final Long TEST_TEAM_ID = 10L;
+    private static final Long TEST_TIME_ID = 20L;
+    private static final Long TEST_QUESTION_ID = 30L;
+    private static final Long TEST_NEW_LEADER_ID = 2L;
+    private static final String TEST_INVITE_CODE = "ABC123";
+    private static final String TEST_TEAM_NAME = "测试队伍";
+
+    private UserVO createTestUser() {
+        return UserVO.builder()
+                .id(TEST_USER_ID)
+                .username("testuser")
+                .roleName("MEMBER")
+                .direction(Direction.COMPUTER_VISION)
+                .build();
+    }
+
+    private UserVO createTestUser(Long userId, String username) {
+        return UserVO.builder()
+                .id(userId)
+                .username(username)
+                .roleName("MEMBER")
+                .direction(Direction.COMPUTER_VISION)
+                .build();
+    }
+
+    private AssessmentTime createTestAssessmentTime(Boolean allowTeam) {
+        return AssessmentTime.reconstruct(
+                TEST_TIME_ID,
+                Direction.COMPUTER_VISION,
+                1,
+                2024,
+                LocalDateTime.of(2099, 1, 1, 9, 0),
+                LocalDateTime.of(2099, 1, 1, 11, 0),
+                false,
+                null,
+                null,
+                allowTeam);
+    }
+
+    private AssessmentTeam createTestTeam() {
+        return AssessmentTeam.reconstruct(
+                TEST_TEAM_ID,
+                TEST_TIME_ID,
+                TEST_USER_ID,
+                TEST_TEAM_NAME,
+                TEST_INVITE_CODE,
+                AssessmentTeam.TeamStatus.ACTIVE,
+                LocalDateTime.now());
+    }
+
+    private AssessmentTeamMember createTestMember(Long id, Long userId) {
+        return AssessmentTeamMember.reconstruct(id, TEST_TEAM_ID, userId, LocalDateTime.now());
+    }
+
+    @Nested
+    @DisplayName("createTeam 方法测试")
+    class CreateTeamTests {
+
+        @Test
+        @DisplayName("正常创建：应返回TeamResult")
+        void createTeam_valid_shouldReturnResult() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser();
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTime time = createTestAssessmentTime(true);
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+                when(assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(false);
+                when(assessmentQuestionRepository.findAllByTimeId(anyLong(), any()))
+                        .thenReturn(new PageImpl<>(Collections.emptyList()));
+                when(assessmentTeamRepository.findByInviteCode(anyString())).thenReturn(Optional.empty());
+                doAnswer(invocation -> {
+                    AssessmentTeam team = invocation.getArgument(0);
+                    team.setId(TEST_TEAM_ID);
+                    return null;
+                }).when(assessmentTeamRepository).save(any(AssessmentTeam.class));
+                when(assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID))
+                        .thenReturn(Collections.emptyList());
+
+                TeamResult result = assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME);
+
+                assertNotNull(result);
+                assertEquals(TEST_TEAM_ID, result.id());
+                assertEquals(TEST_TIME_ID, result.assessmentTimeId());
+                assertEquals(TEST_USER_ID, result.leaderId());
+                assertEquals(TEST_TEAM_NAME, result.name());
+                verify(assessmentTeamRepository).save(any(AssessmentTeam.class));
+            }
+        }
+
+        @Test
+        @DisplayName("未登录：应抛出SecurityException")
+        void createTeam_notAuthenticated_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(null);
+
+                SecurityException ex = assertThrows(
+                        SecurityException.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+                assertEquals("未登录", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("考核时间不存在：应抛出DataNotFound")
+        void createTeam_timeNotFound_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.empty());
+
+                assertThrows(
+                        DataNotFound.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+            }
+        }
+
+        @Test
+        @DisplayName("考核不允许组队：应抛出BadRequest")
+        void createTeam_notAllowTeam_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                AssessmentTime time = createTestAssessmentTime(false);
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+                assertEquals("该考核不允许组队", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("考核已结束：应抛出BadRequest")
+        void createTeam_timeEnded_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                AssessmentTime time = AssessmentTime.reconstruct(
+                        TEST_TIME_ID,
+                        Direction.COMPUTER_VISION,
+                        1,
+                        2024,
+                        LocalDateTime.of(2020, 1, 1, 9, 0),
+                        LocalDateTime.of(2020, 1, 1, 11, 0),
+                        false,
+                        null,
+                        null,
+                        true);
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+                assertEquals("考核时间已结束", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("已加入队伍：应抛出BadRequest")
+        void createTeam_alreadyInTeam_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                AssessmentTime time = createTestAssessmentTime(true);
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+                when(assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(true);
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+                assertEquals("您已加入该考核的队伍", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("已提交个人答案：应抛出BadRequest")
+        void createTeam_hasPersonalAnswer_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                AssessmentTime time = createTestAssessmentTime(true);
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+                when(assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(false);
+
+                AssessmentQuestion question = AssessmentQuestion.reconstruct(
+                        TEST_QUESTION_ID,
+                        TEST_TIME_ID,
+                        1,
+                        QuestionType.FILE_UPLOAD,
+                        null,
+                        null,
+                        null,
+                        null);
+                when(assessmentQuestionRepository.findAllByTimeId(anyLong(), any()))
+                        .thenReturn(new PageImpl<>(List.of(question)));
+                AssessmentAnswer answer = AssessmentAnswer.reconstruct(
+                        100L,
+                        TEST_USER_ID,
+                        TEST_QUESTION_ID,
+                        "content",
+                        null,
+                        null,
+                        LocalDateTime.now(),
+                        null);
+                when(assessmentAnswerRepository.findByUserIdAndQuestionId(TEST_USER_ID, TEST_QUESTION_ID))
+                        .thenReturn(Optional.of(answer));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.createTeam(TEST_TIME_ID, TEST_TEAM_NAME));
+                assertEquals("您已提交过个人答案，无法创建队伍", ex.getMessage());
+            }
+        }
+    }
+
+    @Nested
+    @DisplayName("previewTeam 方法测试")
+    class PreviewTeamTests {
+
+        @Test
+        @DisplayName("正常预览：应返回TeamPreviewResult")
+        void previewTeam_valid_shouldReturnResult() {
+            AssessmentTeam team = createTestTeam();
+            AssessmentTime time = createTestAssessmentTime(true);
+            when(assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE)).thenReturn(Optional.of(team));
+            when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+            when(assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID))
+                    .thenReturn(List.of(createTestMember(1L, TEST_USER_ID)));
+            when(userDomainService.getUser(TEST_USER_ID))
+                    .thenReturn(Optional.of(createTestUser()));
+
+            TeamPreviewResult result = assessmentTeamAppService.previewTeam(TEST_INVITE_CODE);
+
+            assertNotNull(result);
+            assertEquals(TEST_TEAM_ID, result.id());
+            assertEquals(TEST_TEAM_NAME, result.name());
+            assertEquals(1, result.memberCount());
+        }
+
+        @Test
+        @DisplayName("邀请码无效：应抛出DataNotFound")
+        void previewTeam_invalidCode_shouldThrow() {
+            when(assessmentTeamRepository.findByInviteCode("INVALID")).thenReturn(Optional.empty());
+
+            assertThrows(
+                    DataNotFound.class,
+                    () -> assessmentTeamAppService.previewTeam("INVALID"));
+        }
+
+        @Test
+        @DisplayName("考核已结束：应抛出BadRequest")
+        void previewTeam_timeEnded_shouldThrow() {
+            AssessmentTeam team = createTestTeam();
+            AssessmentTime time = AssessmentTime.reconstruct(
+                    TEST_TIME_ID,
+                    Direction.COMPUTER_VISION,
+                    1,
+                    2024,
+                    LocalDateTime.of(2020, 1, 1, 9, 0),
+                    LocalDateTime.of(2020, 1, 1, 11, 0),
+                    false,
+                    null,
+                    null,
+                    true);
+            when(assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE)).thenReturn(Optional.of(team));
+            when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+
+            BadRequest ex = assertThrows(
+                    BadRequest.class,
+                    () -> assessmentTeamAppService.previewTeam(TEST_INVITE_CODE));
+            assertEquals("考核时间已结束", ex.getMessage());
+        }
+    }
+
+    @Nested
+    @DisplayName("joinTeam 方法测试")
+    class JoinTeamTests {
+
+        @Test
+        @DisplayName("正常加入：应返回TeamResult")
+        void joinTeam_valid_shouldReturnResult() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                AssessmentTime time = createTestAssessmentTime(true);
+                when(assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE)).thenReturn(Optional.of(team));
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+                when(assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(false);
+                when(assessmentQuestionRepository.findAllByTimeId(anyLong(), any()))
+                        .thenReturn(new PageImpl<>(Collections.emptyList()));
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID))
+                        .thenReturn(List.of(createTestMember(1L, TEST_USER_ID)));
+
+                TeamResult result = assessmentTeamAppService.joinTeam(TEST_INVITE_CODE);
+
+                assertNotNull(result);
+                verify(assessmentTeamRepository).addMember(TEST_TEAM_ID, TEST_USER_ID);
+            }
+        }
+
+        @Test
+        @DisplayName("队伍已解散：应抛出BadRequest")
+        void joinTeam_disbanded_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = AssessmentTeam.reconstruct(
+                        TEST_TEAM_ID,
+                        TEST_TIME_ID,
+                        TEST_USER_ID,
+                        TEST_TEAM_NAME,
+                        TEST_INVITE_CODE,
+                        AssessmentTeam.TeamStatus.DISBANDED,
+                        LocalDateTime.now());
+                when(assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE)).thenReturn(Optional.of(team));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.joinTeam(TEST_INVITE_CODE));
+                assertEquals("该队伍已解散", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("已加入队伍：应抛出BadRequest")
+        void joinTeam_alreadyInTeam_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                AssessmentTime time = createTestAssessmentTime(true);
+                when(assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE)).thenReturn(Optional.of(team));
+                when(assessmentTimeRepository.findById(TEST_TIME_ID)).thenReturn(Optional.of(time));
+                when(assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(true);
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.joinTeam(TEST_INVITE_CODE));
+                assertEquals("您已加入该考核的队伍", ex.getMessage());
+            }
+        }
+    }
+
+    @Nested
+    @DisplayName("getMyTeam 方法测试")
+    class GetMyTeamTests {
+
+        @Test
+        @DisplayName("已加入队伍：应返回TeamResult")
+        void getMyTeam_hasTeam_shouldReturnResult() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID))
+                        .thenReturn(List.of(createTestMember(1L, TEST_USER_ID)));
+
+                TeamResult result = assessmentTeamAppService.getMyTeam(TEST_TIME_ID);
+
+                assertNotNull(result);
+                assertEquals(TEST_TEAM_ID, result.id());
+            }
+        }
+
+        @Test
+        @DisplayName("未加入队伍：应返回null")
+        void getMyTeam_noTeam_shouldReturnNull() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                when(assessmentTeamRepository.findByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                        .thenReturn(Optional.empty());
+
+                TeamResult result = assessmentTeamAppService.getMyTeam(TEST_TIME_ID);
+
+                assertNull(result);
+            }
+        }
+
+        @Test
+        @DisplayName("未登录：应抛出SecurityException")
+        void getMyTeam_notAuthenticated_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(null);
+
+                SecurityException ex = assertThrows(
+                        SecurityException.class,
+                        () -> assessmentTeamAppService.getMyTeam(TEST_TIME_ID));
+                assertEquals("未登录", ex.getMessage());
+            }
+        }
+    }
+
+    @Nested
+    @DisplayName("leaveTeam 方法测试")
+    class LeaveTeamTests {
+
+        @Test
+        @DisplayName("正常离开：应成功")
+        void leaveTeam_member_shouldSucceed() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser(TEST_NEW_LEADER_ID, "member");
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_NEW_LEADER_ID)).thenReturn(true);
+
+                assessmentTeamAppService.leaveTeam(TEST_TEAM_ID);
+
+                verify(assessmentTeamRepository).removeMember(TEST_TEAM_ID, TEST_NEW_LEADER_ID);
+            }
+        }
+
+        @Test
+        @DisplayName("队长离开：应抛出Forbidden")
+        void leaveTeam_leader_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                Forbidden ex = assertThrows(
+                        Forbidden.class,
+                        () -> assessmentTeamAppService.leaveTeam(TEST_TEAM_ID));
+                assertEquals("队长不能离开队伍，请先转让队长或解散队伍", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("队伍已解散：应抛出BadRequest")
+        void leaveTeam_disbanded_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser(TEST_NEW_LEADER_ID, "member");
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTeam team = AssessmentTeam.reconstruct(
+                        TEST_TEAM_ID,
+                        TEST_TIME_ID,
+                        TEST_USER_ID,
+                        TEST_TEAM_NAME,
+                        TEST_INVITE_CODE,
+                        AssessmentTeam.TeamStatus.DISBANDED,
+                        LocalDateTime.now());
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.leaveTeam(TEST_TEAM_ID));
+                assertEquals("该队伍已解散", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("不是队伍成员：应抛出BadRequest")
+        void leaveTeam_notMember_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser(TEST_NEW_LEADER_ID, "member");
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_NEW_LEADER_ID)).thenReturn(false);
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.leaveTeam(TEST_TEAM_ID));
+                assertEquals("您不是该队伍的成员", ex.getMessage());
+            }
+        }
+    }
+
+    @Nested
+    @DisplayName("transferLeader 方法测试")
+    class TransferLeaderTests {
+
+        @Test
+        @DisplayName("正常转让：应返回TeamResult")
+        void transferLeader_valid_shouldReturnResult() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_NEW_LEADER_ID)).thenReturn(true);
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID))
+                        .thenReturn(
+                                List.of(
+                                        createTestMember(1L, TEST_USER_ID),
+                                        createTestMember(2L, TEST_NEW_LEADER_ID)));
+
+                TeamResult result = assessmentTeamAppService.transferLeader(TEST_TEAM_ID, TEST_NEW_LEADER_ID);
+
+                assertNotNull(result);
+                verify(assessmentTeamRepository).updateLeader(TEST_TEAM_ID, TEST_NEW_LEADER_ID);
+            }
+        }
+
+        @Test
+        @DisplayName("不是队长：应抛出Forbidden")
+        void transferLeader_notLeader_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser(TEST_NEW_LEADER_ID, "member");
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                Forbidden ex = assertThrows(
+                        Forbidden.class,
+                        () -> assessmentTeamAppService.transferLeader(TEST_TEAM_ID, TEST_USER_ID));
+                assertEquals("只有队长可以转让队长", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("新队长不是成员：应抛出BadRequest")
+        void transferLeader_newLeaderNotMember_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+                when(assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_NEW_LEADER_ID)).thenReturn(false);
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.transferLeader(TEST_TEAM_ID, TEST_NEW_LEADER_ID));
+                assertEquals("新队长必须是队伍成员", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("队伍已解散：应抛出BadRequest")
+        void transferLeader_disbanded_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = AssessmentTeam.reconstruct(
+                        TEST_TEAM_ID,
+                        TEST_TIME_ID,
+                        TEST_USER_ID,
+                        TEST_TEAM_NAME,
+                        TEST_INVITE_CODE,
+                        AssessmentTeam.TeamStatus.DISBANDED,
+                        LocalDateTime.now());
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                BadRequest ex = assertThrows(
+                        BadRequest.class,
+                        () -> assessmentTeamAppService.transferLeader(TEST_TEAM_ID, TEST_NEW_LEADER_ID));
+                assertEquals("该队伍已解散", ex.getMessage());
+            }
+        }
+    }
+
+    @Nested
+    @DisplayName("disbandTeam 方法测试")
+    class DisbandTeamTests {
+
+        @Test
+        @DisplayName("正常解散：应成功")
+        void disbandTeam_leader_shouldSucceed() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                assessmentTeamAppService.disbandTeam(TEST_TEAM_ID);
+
+                verify(assessmentTeamRepository).update(any(AssessmentTeam.class));
+            }
+        }
+
+        @Test
+        @DisplayName("不是队长：应抛出Forbidden")
+        void disbandTeam_notLeader_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                UserVO user = createTestUser(TEST_NEW_LEADER_ID, "member");
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(user);
+
+                AssessmentTeam team = createTestTeam();
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.of(team));
+
+                Forbidden ex = assertThrows(
+                        Forbidden.class,
+                        () -> assessmentTeamAppService.disbandTeam(TEST_TEAM_ID));
+                assertEquals("只有队长可以解散队伍", ex.getMessage());
+            }
+        }
+
+        @Test
+        @DisplayName("队伍不存在：应抛出DataNotFound")
+        void disbandTeam_notFound_shouldThrow() {
+            try (MockedStatic<UserCTX> mockedUserCTX = mockStatic(UserCTX.class)) {
+                mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(createTestUser());
+                when(assessmentTeamRepository.findById(TEST_TEAM_ID)).thenReturn(Optional.empty());
+
+                assertThrows(
+                        DataNotFound.class,
+                        () -> assessmentTeamAppService.disbandTeam(TEST_TEAM_ID));
+            }
+        }
+    }
+}
diff --git a/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImplTest.java b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImplTest.java
new file mode 100644
index 0000000..52aa947
--- /dev/null
+++ b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImplTest.java
@@ -0,0 +1,345 @@
+package com.bluenet.web.infrastructure.repository.impl;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+import com.bluenet.web.infrastructure.repository.converter.AssessmentTeamRepositoryConverter;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamDO;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamMemberDO;
+import com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMapper;
+import com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMemberMapper;
+import org.junit.jupiter.api.DisplayName;
+import org.junit.jupiter.api.Nested;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.api.extension.ExtendWith;
+import org.mockito.InjectMocks;
+import org.mockito.Mock;
+import org.mockito.Spy;
+import org.mockito.junit.jupiter.MockitoExtension;
+
+import java.time.LocalDateTime;
+import java.util.Collections;
+import java.util.List;
+import java.util.Optional;
+
+import static org.junit.jupiter.api.Assertions.*;
+import static org.mockito.ArgumentMatchers.*;
+import static org.mockito.Mockito.*;
+
+@DisplayName("AssessmentTeamRepositoryImpl 单元测试")
+@ExtendWith(MockitoExtension.class)
+class AssessmentTeamRepositoryImplTest {
+
+    @Mock
+    private AssessmentTeamMapper assessmentTeamMapper;
+
+    @Mock
+    private AssessmentTeamMemberMapper assessmentTeamMemberMapper;
+
+    @Spy
+    private AssessmentTeamRepositoryConverter converter = new AssessmentTeamRepositoryConverter();
+
+    @InjectMocks
+    private AssessmentTeamRepositoryImpl assessmentTeamRepository;
+
+    private static final Long TEST_TEAM_ID = 10L;
+    private static final Long TEST_USER_ID = 1L;
+    private static final Long TEST_TIME_ID = 20L;
+    private static final String TEST_INVITE_CODE = "ABC123";
+
+    private AssessmentTeamDO createTestTeamDO() {
+        return AssessmentTeamDO.builder()
+                .id(TEST_TEAM_ID)
+                .assessmentTimeId(TEST_TIME_ID)
+                .leaderId(TEST_USER_ID)
+                .name("测试队伍")
+                .inviteCode(TEST_INVITE_CODE)
+                .status("ACTIVE")
+                .createdAt(LocalDateTime.now())
+                .build();
+    }
+
+    private AssessmentTeamMemberDO createTestMemberDO(Long id, Long userId) {
+        return AssessmentTeamMemberDO.builder()
+                .id(id)
+                .teamId(TEST_TEAM_ID)
+                .userId(userId)
+                .joinedAt(LocalDateTime.now())
+                .build();
+    }
+
+    @Nested
+    @DisplayName("findById 方法测试")
+    class FindByIdTests {
+
+        @Test
+        @DisplayName("队伍存在：应返回实体")
+        void findById_existing_shouldReturnEntity() {
+            when(assessmentTeamMapper.selectById(TEST_TEAM_ID)).thenReturn(createTestTeamDO());
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository.findById(TEST_TEAM_ID);
+
+            assertTrue(result.isPresent());
+            assertEquals(TEST_TEAM_ID, result.get().getId());
+            assertEquals(TEST_USER_ID, result.get().getLeaderId());
+        }
+
+        @Test
+        @DisplayName("队伍不存在：应返回空")
+        void findById_notExisting_shouldReturnEmpty() {
+            when(assessmentTeamMapper.selectById(TEST_TEAM_ID)).thenReturn(null);
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository.findById(TEST_TEAM_ID);
+
+            assertTrue(result.isEmpty());
+        }
+    }
+
+    @Nested
+    @DisplayName("findByInviteCode 方法测试")
+    class FindByInviteCodeTests {
+
+        @Test
+        @DisplayName("邀请码存在：应返回实体")
+        void findByInviteCode_existing_shouldReturnEntity() {
+            when(assessmentTeamMapper.selectByInviteCode(TEST_INVITE_CODE)).thenReturn(createTestTeamDO());
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository.findByInviteCode(TEST_INVITE_CODE);
+
+            assertTrue(result.isPresent());
+            assertEquals(TEST_INVITE_CODE, result.get().getInviteCode());
+        }
+
+        @Test
+        @DisplayName("邀请码不存在：应返回空")
+        void findByInviteCode_notExisting_shouldReturnEmpty() {
+            when(assessmentTeamMapper.selectByInviteCode("INVALID")).thenReturn(null);
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository.findByInviteCode("INVALID");
+
+            assertTrue(result.isEmpty());
+        }
+    }
+
+    @Nested
+    @DisplayName("findByAssessmentTimeIdAndUserId 方法测试")
+    class FindByAssessmentTimeIdAndUserIdTests {
+
+        @Test
+        @DisplayName("用户已加入队伍：应返回实体")
+        void findByAssessmentTimeIdAndUserId_existing_shouldReturnEntity() {
+            when(assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                    .thenReturn(createTestTeamDO());
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository
+                    .findByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID);
+
+            assertTrue(result.isPresent());
+            assertEquals(TEST_TIME_ID, result.get().getAssessmentTimeId());
+        }
+
+        @Test
+        @DisplayName("用户未加入队伍：应返回空")
+        void findByAssessmentTimeIdAndUserId_notExisting_shouldReturnEmpty() {
+            when(assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                    .thenReturn(null);
+
+            Optional<AssessmentTeam> result = assessmentTeamRepository
+                    .findByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID);
+
+            assertTrue(result.isEmpty());
+        }
+    }
+
+    @Nested
+    @DisplayName("existsByAssessmentTimeIdAndUserId 方法测试")
+    class ExistsByAssessmentTimeIdAndUserIdTests {
+
+        @Test
+        @DisplayName("用户已加入队伍：应返回true")
+        void existsByAssessmentTimeIdAndUserId_existing_shouldReturnTrue() {
+            when(assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                    .thenReturn(createTestTeamDO());
+
+            boolean result = assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID);
+
+            assertTrue(result);
+        }
+
+        @Test
+        @DisplayName("用户未加入队伍：应返回false")
+        void existsByAssessmentTimeIdAndUserId_notExisting_shouldReturnFalse() {
+            when(assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID))
+                    .thenReturn(null);
+
+            boolean result = assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(TEST_TIME_ID, TEST_USER_ID);
+
+            assertFalse(result);
+        }
+    }
+
+    @Nested
+    @DisplayName("save 方法测试")
+    class SaveTests {
+
+        @Test
+        @DisplayName("保存队伍：应插入队伍和队长成员")
+        void save_valid_shouldInsertTeamAndLeaderMember() {
+            AssessmentTeam team = AssessmentTeam.create(TEST_TIME_ID, TEST_USER_ID, "测试队伍", "XYZ789");
+            when(assessmentTeamMapper.insert(any(AssessmentTeamDO.class))).thenAnswer(invocation -> {
+                AssessmentTeamDO dataObject = invocation.getArgument(0);
+                dataObject.setId(TEST_TEAM_ID);
+                return 1;
+            });
+
+            assessmentTeamRepository.save(team);
+
+            assertEquals(TEST_TEAM_ID, team.getId());
+            verify(assessmentTeamMapper).insert(any(AssessmentTeamDO.class));
+            verify(assessmentTeamMemberMapper).insert(any(AssessmentTeamMemberDO.class));
+        }
+    }
+
+    @Nested
+    @DisplayName("update 方法测试")
+    class UpdateTests {
+
+        @Test
+        @DisplayName("更新队伍：应调用updateById")
+        void update_valid_shouldCallUpdateById() {
+            AssessmentTeam team = AssessmentTeam.reconstruct(
+                    TEST_TEAM_ID,
+                    TEST_TIME_ID,
+                    TEST_USER_ID,
+                    "新名称",
+                    TEST_INVITE_CODE,
+                    AssessmentTeam.TeamStatus.DISBANDED,
+                    LocalDateTime.now());
+
+            assessmentTeamRepository.update(team);
+
+            verify(assessmentTeamMapper).updateById(any(AssessmentTeamDO.class));
+        }
+    }
+
+    @Nested
+    @DisplayName("deleteById 方法测试")
+    class DeleteByIdTests {
+
+        @Test
+        @DisplayName("删除队伍：应先删除成员再删除队伍")
+        void deleteById_valid_shouldDeleteMembersThenTeam() {
+            assessmentTeamRepository.deleteById(TEST_TEAM_ID);
+
+            verify(assessmentTeamMemberMapper).delete(any());
+            verify(assessmentTeamMapper).deleteById(TEST_TEAM_ID);
+        }
+    }
+
+    @Nested
+    @DisplayName("updateLeader 方法测试")
+    class UpdateLeaderTests {
+
+        @Test
+        @DisplayName("转让队长：应调用updateLeader")
+        void updateLeader_valid_shouldCallMapper() {
+            Long newLeaderId = 2L;
+            when(assessmentTeamMapper.updateLeader(TEST_TEAM_ID, newLeaderId)).thenReturn(1);
+
+            assessmentTeamRepository.updateLeader(TEST_TEAM_ID, newLeaderId);
+
+            verify(assessmentTeamMapper).updateLeader(TEST_TEAM_ID, newLeaderId);
+        }
+    }
+
+    @Nested
+    @DisplayName("addMember 方法测试")
+    class AddMemberTests {
+
+        @Test
+        @DisplayName("添加成员：应插入成员记录")
+        void addMember_valid_shouldInsertMember() {
+            Long newUserId = 2L;
+
+            assessmentTeamRepository.addMember(TEST_TEAM_ID, newUserId);
+
+            verify(assessmentTeamMemberMapper).insert(
+                    argThat(
+                            (AssessmentTeamMemberDO dataObject) -> dataObject.getTeamId().equals(TEST_TEAM_ID)
+                                    && dataObject.getUserId().equals(newUserId)));
+        }
+    }
+
+    @Nested
+    @DisplayName("removeMember 方法测试")
+    class RemoveMemberTests {
+
+        @Test
+        @DisplayName("移除成员：应调用deleteByTeamIdAndUserId")
+        void removeMember_valid_shouldCallDelete() {
+            Long memberId = 2L;
+
+            assessmentTeamRepository.removeMember(TEST_TEAM_ID, memberId);
+
+            verify(assessmentTeamMemberMapper).deleteByTeamIdAndUserId(TEST_TEAM_ID, memberId);
+        }
+    }
+
+    @Nested
+    @DisplayName("findMembersByTeamId 方法测试")
+    class FindMembersByTeamIdTests {
+
+        @Test
+        @DisplayName("有成员：应返回成员列表")
+        void findMembersByTeamId_withMembers_shouldReturnList() {
+            when(assessmentTeamMemberMapper.selectByTeamId(TEST_TEAM_ID))
+                    .thenReturn(
+                            List.of(
+                                    createTestMemberDO(1L, TEST_USER_ID),
+                                    createTestMemberDO(2L, 2L)));
+
+            List<AssessmentTeamMember> result = assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID);
+
+            assertEquals(2, result.size());
+            assertEquals(TEST_USER_ID, result.get(0).getUserId());
+            assertEquals(2L, result.get(1).getUserId());
+        }
+
+        @Test
+        @DisplayName("无成员：应返回空列表")
+        void findMembersByTeamId_noMembers_shouldReturnEmptyList() {
+            when(assessmentTeamMemberMapper.selectByTeamId(TEST_TEAM_ID))
+                    .thenReturn(Collections.emptyList());
+
+            List<AssessmentTeamMember> result = assessmentTeamRepository.findMembersByTeamId(TEST_TEAM_ID);
+
+            assertTrue(result.isEmpty());
+        }
+    }
+
+    @Nested
+    @DisplayName("isMember 方法测试")
+    class IsMemberTests {
+
+        @Test
+        @DisplayName("是成员：应返回true")
+        void isMember_yes_shouldReturnTrue() {
+            when(assessmentTeamMemberMapper.existsByTeamIdAndUserId(TEST_TEAM_ID, TEST_USER_ID))
+                    .thenReturn(true);
+
+            boolean result = assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_USER_ID);
+
+            assertTrue(result);
+        }
+
+        @Test
+        @DisplayName("不是成员：应返回false")
+        void isMember_no_shouldReturnFalse() {
+            when(assessmentTeamMemberMapper.existsByTeamIdAndUserId(TEST_TEAM_ID, TEST_USER_ID))
+                    .thenReturn(false);
+
+            boolean result = assessmentTeamRepository.isMember(TEST_TEAM_ID, TEST_USER_ID);
+
+            assertFalse(result);
+        }
+    }
+}
```

### `f964bb20` feat: 实现考核系统组队支持功能

- **时间:** 2026-05-16 20:45:54 +0800

**提交信息:**

feat: 实现考核系统组队支持功能

- 新增考核组队全流程能力，包括创建/加入/退出/转让/解散队伍
- 为考核时间新增allowTeam字段，支持配置是否允许组队
- 新增队伍相关数据库表和持久层逻辑
- 调整考核时间查询逻辑，支持跨方向考核
- 前端新增组队相关UI和交互逻辑
- 完善答题和评分的组队相关校验逻辑

**代码变更:**

```diff
diff --git a/openspec/changes/assessment-team-support/.openspec.yaml b/openspec/changes/assessment-team-support/.openspec.yaml
new file mode 100644
index 0000000..ab7f13b
--- /dev/null
+++ b/openspec/changes/assessment-team-support/.openspec.yaml
@@ -0,0 +1,2 @@
+schema: spec-driven
+created: 2026-05-16
diff --git a/openspec/changes/assessment-team-support/design.md b/openspec/changes/assessment-team-support/design.md
new file mode 100644
index 0000000..c58f7bc
--- /dev/null
+++ b/openspec/changes/assessment-team-support/design.md
@@ -0,0 +1,108 @@
+## Context
+
+当前考核系统中，考核时间按 `(direction, epoch, grade)` 组织，答案按 `user_id + question_id` 关联。所有题目均为个人作答，没有组队机制。
+
+蓝网团队的最终考核涉及跨方向项目（如智能小车），需要 CV、电控、机械结构三个方向协作完成一个作品。现有系统无法支持：
+- 不同方向考生参与同一个考核
+- 多人协作提交同一份作品
+- 同一份作品对不同队员独立评分
+
+## Goals / Non-Goals
+
+**Goals:**
+- 考核时间支持配置"允许组队"，仅限 FILE_UPLOAD 题可组队
+- 跨方向考核通过 `direction = null` 实现，所有方向考生可见
+- 队伍绑定考核轮次，考核结束后自动解散
+- 邀请码加入流程：输入邀请码 → 预览队伍信息 → 确认加入
+- 仅队长可提交/更新组队题答案，队员可查看
+- 评委对同一份作品给每个队员独立评分、独立做录用决策
+- 接口复用现有 `UserInfo` DTO，避免重复定义用户字段
+
+**Non-Goals:**
+- 不实现邀请链接功能（通过 URL 参数自动加入），本次仅支持邀请码
+- 不实现队伍实时通信（聊天、协作编辑）
+- 不限制队伍人数上限（初期不设限，可后续增加）
+- 不实现算法题/选择题的组队支持
+- 不支持部分题目组队、部分题目个人作答的混合模式（一个考核要么全组队要么全个人）
+
+## Decisions
+
+### Decision: 队伍绑定考核轮次而非全局存在
+**选择**：队伍数据模型包含 `assessment_time_id`，每次考核单独创建队伍。  
+**理由**：
+- 用户明确表示"队伍跟着考核轮次，考核结束后自动解散"
+- 不同考核可以不同组队，上一轮被淘汰的人下一轮可以和别人组
+- 避免全局队伍的权限管理和生命周期复杂度
+
+**替代方案**：全局队伍 + 考核内报名。放弃原因：需要两层关系（全局队伍 + 考核实例），模型复杂度高，与需求不符。
+
+### Decision: `direction = null` 表示跨方向共享
+**选择**：考核时间的 `direction` 字段为 `null` 时，所有方向考生可见。  
+**理由**：
+- 复用现有字段语义，无需新增"是否跨方向"字段
+- 与现有最终考核的语义一致
+- `grade` 仍然有效，用于限制年级
+
+**影响**：需要修改 `AssessmentTimeMapper.xml` 的 `selectPageByUserParticipation`，增加 `OR (t.direction IS NULL AND t.grade = #{enrollmentYear})` 分支。
+
+### Decision: 答案表加 `team_id` 而非独立表存储组队答案
+**选择**：在 `tb_assessment_answer` 增加 `team_id` 字段，队长提交时记录 `team_id`，队员查询时通过 `team_id` 关联到队长的答案。  
+**理由**：
+- 最小化数据模型改动
+- 非组队题 `team_id = null`，完全兼容现有逻辑
+- 评分表 `tb_assessment_judgement` 已有 `user_id` 字段，可以独立给每个队员评分
+
+**替代方案**：新建 `tb_team_answer` 表。放弃原因：增加一层关联查询复杂度，收益不大。
+
+### Decision: 邀请码预览接口独立于加入接口
+**选择**：
+- `POST /api/v1/assessment-teams/preview` — 输入邀请码，返回队伍信息（不修改数据）
+- `POST /api/v1/assessment-teams/join` — 确认加入，真正写入数据  
+**理由**：
+- 用户明确要求"先告诉用户他现在会被邀请到哪一组，有谁，然后确认加入才能加入"
+- 预览接口无副作用，可以安全地多次调用
+- 前端可以在输入邀请码后实时展示预览，用户确认后再调用 join
+
+### Decision: 复用 `UserInfo` 展示队伍成员
+**选择**：队伍成员列表接口返回 `List<UserInfo>` 或类似结构，复用现有的用户信息字段（`id`, `username`, `direction`, `avatar` 等）。  
+**理由**：
+- 用户明确要求"接口应该尽可能复用现有DTO，如UserInfo等"
+- 避免新建 `TeamMemberDTO` 重复定义用户字段
+- 前端可直接使用已有的用户展示组件
+
+### Decision: 评分保持 `user_id` 粒度，不按 `team_id`
+**选择**：`tb_assessment_judgement` 的 `user_id` 记录被评分人，`answer_id` 关联到队长的答案。每个队员一条独立 judgement 记录。  
+**理由**：
+- 用户明确要求"每个人具有独立的得分，一个小队可以只录用其中某个人"
+- 复用现有评分模型，无需改动 judgement 表结构
+- 评委在评分时选择具体的人进行评分
+
+## Risks / Trade-offs
+
+**[Risk] `direction = null` 的考核时间可能被管理员误创建为跨方向**  
+→ **Mitigation**: 管理端创建页面增加明显提示："方向为空表示跨方向共享，所有方向考生可见"
+
+**[Risk] 队长退出或账号异常导致队伍无法提交**  
+→ **Mitigation**: 队长退出前必须先转让队长身份；不允许队长直接退出。如果队长账号被删除，由管理员手动转让队长（管理端接口）。
+
+**[Risk] 队员看到"队长已提交"后，队长又修改了答案，队员看到的是旧版本**  
+→ **Mitigation**: 队员查询答案时实时查询，不做缓存；前端加入轮询或提交后通知机制。
+
+**[Risk] 同一个考核中，用户先个人提交了 FILE_UPLOAD 题，后来又组队**  
+→ **Mitigation**: 用户在该考核中已有答案记录时，禁止其创建/加入队伍。或者：加入队伍后，个人答案自动归并到队伍答案（取最新）。**当前方案**：已有答案的用户不能创建/加入队伍，需先删除个人答案。
+
+**[Risk] 非 FILE_UPLOAD 题在 allow_team=true 的考核中如何处理**  
+→ **Mitigation**: 非 FILE_UPLOAD 题不受组队影响，仍按个人答题处理。考题目录页中 FILE_UPLOAD 题显示组队相关UI，其他题正常显示。
+
+## Migration Plan
+
+1. **数据库迁移**：Flyway 脚本新增 `tb_assessment_team`、`tb_assessment_team_member`；修改 `tb_assessment_time`（加 `allow_team`）、`tb_assessment_answer`（加 `team_id`）
+2. **后端部署**：新增表和接口后，旧代码兼容（`allow_team` 默认 `false`，`team_id` 默认 `null`）
+3. **前端部署**：管理端新增"允许组队"开关；用户端组队相关UI按需加载
+4. **回滚**：关闭所有考核的 `allow_team` 即可，已有队伍数据保留但不影响逻辑
+
+## Open Questions
+
+1. 队伍名称是否必填？是否有默认生成规则？
+2. 一个考核中是否允许存在多个 FILE_UPLOAD 题？如果允许多道组队题，队伍是否需要按题细分？
+3. 队长修改答案后，已出的评分是否需要重新评？
diff --git a/openspec/changes/assessment-team-support/proposal.md b/openspec/changes/assessment-team-support/proposal.md
new file mode 100644
index 0000000..ce4169c
--- /dev/null
+++ b/openspec/changes/assessment-team-support/proposal.md
@@ -0,0 +1,31 @@
+## Why
+
+当前考核系统仅支持个人答题，但团队项目（如智能小车）需要计算机视觉、电控、机械结构三个方向协作完成。缺乏组队机制导致跨方向考核无法有效组织，不同方向考生无法共享同一份作品提交和评分。
+
+## What Changes
+
+- **新增考核组队能力**：考核时间支持开启"允许组队"，仅限 FILE_UPLOAD 类型题目可组队作答。
+- **新增队伍生命周期管理**：创建队伍、邀请码加入、退出/转让/解散队伍，队伍绑定考核轮次，考核结束后自动解散。
+- **新增邀请码预览确认流程**：输入邀请码后先展示队伍信息（名称、成员列表），用户确认后才正式加入。
+- **跨方向考核共享**：`direction` 为 `null` 的考核时间对所有方向可见，支持跨方向组队。
+- **队长唯一提交权限**：组队题仅队长可上传作品，队员可查看但不可修改。
+- **独立评分与录用**：同一份作品，评委对每个队员独立评分、独立决定录用/淘汰。
+- **修改考核时间查询逻辑**：用户端查询支持返回 `direction = null` 的跨方向考核。
+- **修改答题校验逻辑**：FILE_UPLOAD 题在允许组队的考核中，校验队长权限后才可提交/更新。
+
+## Capabilities
+
+### New Capabilities
+- `assessment-team-support`: 考核组队全生命周期管理，包括创建队伍、邀请码加入、预览确认、退出/转让/解散、队长提交权限控制。
+
+### Modified Capabilities
+- `assessment-time-management`: 新增 `allow_team` 字段；创建/编辑考核时支持设置是否允许组队；查询逻辑支持 `direction = null`。
+- `frontend-assessment-question-page`: FILE_UPLOAD 题在组队考核中增加组队前置流程；题目页根据队长/队员角色展示不同操作区。
+- `assessment-judgement`: 评分和评论按 `user_id` 独立记录，同一队伍成员共享同一份 `answer_id` 但各自有独立的 `judgement` 记录。
+
+## Impact
+
+- **后端**：新增 `tb_assessment_team`、`tb_assessment_team_member` 表；修改 `tb_assessment_time`（加 `allow_team`）、`tb_assessment_answer`（加 `team_id`）；新增 `AssessmentTeamController`、`AssessmentTeamAppService`；修改 `AssessmentTimeAppServiceImpl`（查询逻辑）、`AssessmentAnswerAppServiceImpl`（提交校验）。
+- **前端**：考核时间管理页面增加"允许组队"开关；考题目录页增加组队状态判断；FILE_UPLOAD 题页面增加队伍信息面板、邀请码输入/展示、队长上传区/队员只读区。
+- **数据库**：新增两张表，修改两张表，需编写 Flyway 迁移脚本。
+- **接口复用**：队伍成员信息复用现有的 `UserInfo` DTO 结构，避免重复定义用户字段。
diff --git a/openspec/changes/assessment-team-support/specs/assessment-judgement/spec.md b/openspec/changes/assessment-team-support/specs/assessment-judgement/spec.md
new file mode 100644
index 0000000..fcd22be
--- /dev/null
+++ b/openspec/changes/assessment-team-support/specs/assessment-judgement/spec.md
@@ -0,0 +1,60 @@
+## ADDED Requirements
+
+### Requirement: 组队题评分按队员独立记录
+对于 FILE_UPLOAD 类型的组队题，系统 SHALL 允许评委对同一份答案的每个队员独立评分、独立评论。每个队员 SHALL 有独立的 `tb_assessment_judgement` 记录，共享同一个 `answer_id` 但具有不同的 `user_id`。
+
+#### Scenario: 评委给队长评分
+- **WHEN** 评委对 FILE_UPLOAD 组队题的队长进行评分
+- **THEN** 系统 SHALL 创建一条 judgement 记录，`answer_id` 为队长的答案，`user_id` 为队长 ID
+
+#### Scenario: 评委给队员评分
+- **WHEN** 评委对同一 FILE_UPLOAD 组队题的队员进行评分
+- **THEN** 系统 SHALL 创建另一条 judgement 记录，`answer_id` 仍为队长的答案（同一份作品），但 `user_id` 为该队员 ID
+
+#### Scenario: 不同队员得分不同
+- **WHEN** 评委给队长打 85 分，给队员 A 打 82 分，给队员 B 打 78 分
+- **THEN** 系统 SHALL 保存三条独立的 judgement 记录，各自具有不同的分数
+
+### Requirement: 组队题答案查询返回队长作品
+评委查询 FILE_UPLOAD 组队题的答案时，系统 SHALL 返回队长提交的作品（`answer_id` 关联到队长）。评委评分时 SHALL 明确指定被评分人（`user_id`）。
+
+#### Scenario: 评委查看组队题答案
+- **WHEN** 评委查询某 FILE_UPLOAD 组队题的答案
+- **THEN** 系统 SHALL 返回队长提交的答案及文件信息
+
+#### Scenario: 评委选择队员进行评分
+- **WHEN** 评委在评分界面选择某个队员进行评分
+- **THEN** 系统 SHALL 将该评分关联到该队员的 `user_id`
+
+## MODIFIED Requirements
+
+### Requirement: Manual review for file upload answers
+系统 SHALL 允许具有 team member 或更高权限的用户对文件上传答案进行评分和评论。对于组队题，评分 SHALL 针对具体队员，每个队员有独立的评分记录。
+
+#### Scenario: Member scores file upload answer
+- **WHEN** team member 为文件上传答案提交有效分数和评论
+- **THEN** 系统 SHALL 保存人工评分，并在答案评审视图中展示
+- **AND** 系统 SHALL 同时在 `tb_comment` 中保存评论记录以便多评审者可见
+
+#### Scenario: Member scores team member individually
+- **WHEN** team member 为 FILE_UPLOAD 组队题的某个队员进行评分
+- **THEN** 系统 SHALL 保存该评分并关联到该队员的 `user_id`，不影响其他队员的评分
+
+#### Scenario: Candidate cannot score file upload answer
+- **WHEN** candidate 尝试为任何文件上传答案评分
+- **THEN** 系统 SHALL 拒绝该操作并返回 forbidden 响应
+
+### Requirement: Judgement result visibility
+系统 SHALL 允许考生查看自己的评分结果，允许 team member 或更高角色在其授权范围内查看考生的评分结果。对于组队题，考生 SHALL 只能看到自己的评分，不能看到队友的评分。
+
+#### Scenario: Candidate views own result
+- **WHEN** candidate 请求查看自己提交的答案的评分结果
+- **THEN** 系统 SHALL 返回该 candidate 的评分结果
+
+#### Scenario: Team member views candidate result
+- **WHEN** team member 在其授权的考核范围内请求查看 candidate 的评分结果
+- **THEN** 系统 SHALL 返回匹配的 candidate 评分结果
+
+#### Scenario: Team member cannot view teammate's result
+- **WHEN** candidate（队员）尝试查看队友的评分结果
+- **THEN** 系统 SHALL 返回 403 错误，提示只能查看自己的评分
diff --git a/openspec/changes/assessment-team-support/specs/assessment-team-support/spec.md b/openspec/changes/assessment-team-support/specs/assessment-team-support/spec.md
new file mode 100644
index 0000000..449ba61
--- /dev/null
+++ b/openspec/changes/assessment-team-support/specs/assessment-team-support/spec.md
@@ -0,0 +1,139 @@
+## ADDED Requirements
+
+### Requirement: 创建考核队伍
+系统 SHALL 允许已登录用户在允许组队的考核中创建队伍。创建时 MUST 校验该用户当前在该考核中未加入任何队伍，且该考核 `allow_team = true`。
+
+创建成功后，系统 SHALL 自动生成唯一邀请码（6位字母数字），并将创建者设为队长。
+
+#### Scenario: 成功创建队伍
+- **WHEN** 用户在 `allow_team = true` 的考核中请求创建队伍
+- **THEN** 系统 SHALL 创建队伍记录，设置 `leader_id` 为该用户，`invite_code` 为自动生成的唯一码，并返回队伍信息（含邀请码）
+
+#### Scenario: 考核不允许组队
+- **WHEN** 用户请求在 `allow_team = false` 的考核中创建队伍
+- **THEN** 系统 SHALL 返回 400 错误，提示该考核不支持组队
+
+#### Scenario: 用户已在该考核中有队伍
+- **WHEN** 用户请求创建队伍，但该用户已在该考核中属于某个队伍
+- **THEN** 系统 SHALL 返回 409 Conflict 错误，提示用户已有队伍
+
+#### Scenario: 用户已有个人答案
+- **WHEN** 用户请求创建队伍，但该用户已在该考核的 FILE_UPLOAD 题上提交了个人答案
+- **THEN** 系统 SHALL 返回 409 Conflict 错误，提示已有个人答案，无法组队
+
+### Requirement: 邀请码预览队伍信息
+系统 SHALL 提供无副作用的预览接口，用户输入邀请码后可查看队伍信息（队伍名称、队长、成员列表），但不加入队伍。
+
+预览接口返回的成员列表 SHALL 复用现有的 `UserInfo` 结构，包含用户基本信息（`id`, `username`, `direction`, `avatar` 等）。
+
+#### Scenario: 有效邀请码预览
+- **WHEN** 用户提交有效的邀请码
+- **THEN** 系统 SHALL 返回对应队伍的名称、队长信息、当前成员列表，且 SHALL NOT 修改任何数据
+
+#### Scenario: 无效邀请码预览
+- **WHEN** 用户提交不存在的邀请码
+- **THEN** 系统 SHALL 返回 404 错误，提示邀请码无效
+
+#### Scenario: 邀请码已过期
+- **WHEN** 用户提交对应考核已结束的邀请码
+- **THEN** 系统 SHALL 返回 400 错误，提示该邀请码已过期
+
+### Requirement: 通过邀请码加入队伍
+系统 SHALL 允许已登录用户通过邀请码加入队伍。加入前用户 MUST 在预览后显式确认。
+
+加入时 SHALL 校验：
+- 邀请码存在且对应考核未结束
+- 用户未在该考核中加入其他队伍
+- 用户在该考核的 FILE_UPLOAD 题上无个人答案记录
+
+#### Scenario: 成功加入队伍
+- **WHEN** 用户提交有效邀请码并确认加入
+- **THEN** 系统 SHALL 将用户加入队伍成员列表，并返回更新后的队伍信息
+
+#### Scenario: 用户已在其他队伍
+- **WHEN** 用户尝试加入队伍，但该用户已在同一考核的其他队伍中
+- **THEN** 系统 SHALL 返回 409 Conflict 错误，提示用户已有队伍
+
+#### Scenario: 用户已有个人答案
+- **WHEN** 用户尝试加入队伍，但该用户已在该考核的 FILE_UPLOAD 题上提交了个人答案
+- **THEN** 系统 SHALL 返回 409 Conflict 错误，提示已有个人答案，无法加入队伍
+
+### Requirement: 查询当前用户的队伍
+系统 SHALL 提供接口查询当前用户在指定考核中的队伍信息，包括队伍名称、队长、成员列表、邀请码。
+
+成员列表 SHALL 复用现有的 `UserInfo` 结构。
+
+#### Scenario: 用户已组队
+- **WHEN** 用户查询自己在某考核中的队伍
+- **THEN** 系统 SHALL 返回队伍详情及成员列表
+
+#### Scenario: 用户未组队
+- **WHEN** 用户查询自己在某考核中的队伍，但该用户未加入任何队伍
+- **THEN** 系统 SHALL 返回 404 或空数据，表示未组队
+
+### Requirement: 退出队伍
+系统 SHALL 允许队员退出队伍。队长 MUST NOT 直接退出，必须先转让队长身份。
+
+退出后，该用户 SHALL 恢复为未组队状态，可重新创建或加入其他队伍（考核未结束前提下）。
+
+#### Scenario: 队员成功退出
+- **WHEN** 队员请求退出队伍
+- **THEN** 系统 SHALL 从队伍成员列表中移除该用户
+
+#### Scenario: 队长直接退出被拒绝
+- **WHEN** 队长请求退出队伍但未转让队长身份
+- **THEN** 系统 SHALL 返回 403 错误，提示队长需先转让队长身份
+
+### Requirement: 转让队长身份
+系统 SHALL 允许队长将队长身份转让给其他队员。转让后原队长变为普通队员。
+
+#### Scenario: 队长成功转让
+- **WHEN** 队长将队长身份转让给另一名队员
+- **THEN** 系统 SHALL 更新 `leader_id` 为目标用户，并返回更新后的队伍信息
+
+#### Scenario: 非队长尝试转让
+- **WHEN** 非队长用户尝试转让队长身份
+- **THEN** 系统 SHALL 返回 403 错误
+
+#### Scenario: 转让给非队员
+- **WHEN** 队长尝试将队长身份转让给不在该队伍中的用户
+- **THEN** 系统 SHALL 返回 400 错误
+
+### Requirement: 队长提交组队题答案
+在允许组队的考核中，FILE_UPLOAD 类型的题目仅队长有权提交和更新答案。队员 SHALL 只能查看队长提交的文件，不可修改。
+
+提交时，答案记录的 `team_id` SHALL 设为当前队伍 ID，`user_id` SHALL 设为队长 ID。
+
+#### Scenario: 队长提交组队题答案
+- **WHEN** 队长提交 FILE_UPLOAD 题答案
+- **THEN** 系统 SHALL 保存答案，设置 `team_id` 为队伍 ID，返回成功
+
+#### Scenario: 队员尝试提交组队题答案
+- **WHEN** 队员尝试提交 FILE_UPLOAD 题答案
+- **THEN** 系统 SHALL 返回 403 错误，提示仅队长可提交
+
+#### Scenario: 非组队题不受限制
+- **WHEN** 用户在允许组队的考核中提交非 FILE_UPLOAD 题答案
+- **THEN** 系统 SHALL 按个人答题正常处理，不校验队伍和队长权限
+
+### Requirement: 队员查看组队题答案
+队员 SHALL 通过队伍关联查看队长提交的 FILE_UPLOAD 题答案。查询接口 SHALL 根据当前用户的 `team_id` 返回队长的答案。
+
+#### Scenario: 队员查看组队题答案
+- **WHEN** 队员查询自己在某 FILE_UPLOAD 题的答案
+- **THEN** 系统 SHALL 返回队长提交的答案（file_id、content 等）
+
+#### Scenario: 未组队用户查看组队题答案
+- **WHEN** 未组队的用户查询 FILE_UPLOAD 题答案且该考核允许组队
+- **THEN** 系统 SHALL 返回 404 或提示需要先组队
+
+### Requirement: 考核结束后队伍自动解散
+系统 SHALL 在考核结束后将相关队伍状态置为 `DISBANDED`，禁止后续加入、退出、提交等操作。
+
+#### Scenario: 考核结束后提交被拒绝
+- **WHEN** 用户在已结束的考核中尝试提交答案
+- **THEN** 系统 SHALL 返回 400 错误，提示考核已结束
+
+#### Scenario: 考核结束后加入队伍被拒绝
+- **WHEN** 用户尝试加入已结束考核的队伍
+- **THEN** 系统 SHALL 返回 400 错误，提示考核已结束
diff --git a/openspec/changes/assessment-team-support/specs/assessment-time-management/spec.md b/openspec/changes/assessment-team-support/specs/assessment-time-management/spec.md
new file mode 100644
index 0000000..ce7fb5c
--- /dev/null
+++ b/openspec/changes/assessment-team-support/specs/assessment-time-management/spec.md
@@ -0,0 +1,64 @@
+## ADDED Requirements
+
+### Requirement: 考核时间支持允许组队配置
+系统 SHALL 在 `tb_assessment_time` 表中增加 `allow_team` 字段（BOOLEAN, DEFAULT FALSE），用于标识该考核是否允许组队答题。
+
+创建和更新考核时间时，管理端接口 SHALL 支持传入 `allowTeam` 参数。响应 DTO SHALL 包含 `allowTeam` 字段。
+
+#### Scenario: 创建允许组队的考核时间
+- **WHEN** 管理员创建考核时间并设置 `allowTeam = true`
+- **THEN** 系统 SHALL 保存 `allow_team = true`，并返回包含 `allowTeam` 字段的 DTO
+
+#### Scenario: 响应 DTO 包含 allowTeam
+- **WHEN** 查询或创建考核时间成功
+- **THEN** 响应 SHALL 包含 `allowTeam` 字段
+
+### Requirement: 跨方向考核时间对所有方向可见
+当 `tb_assessment_time.direction` 为 `null` 时，该考核时间 SHALL 对所有方向的已登录用户可见（仍需匹配 `grade`）。
+
+用户端查询接口 `GET /api/v1/assessment-times` 的过滤逻辑 SHALL 增加对 `direction IS NULL` 的支持。
+
+#### Scenario: 跨方向考核对 CV 方向考生可见
+- **WHEN** CV 方向考生查询考核时间列表，且存在 `direction = null, grade = 2025` 的考核
+- **THEN** 系统 SHALL 返回该考核时间
+
+#### Scenario: 跨方向考核对电控方向成员可见
+- **WHEN** 电控方向成员查询考核时间列表，且存在 `direction = null` 的考核
+- **THEN** 系统 SHALL 返回该考核时间
+
+#### Scenario: 普通方向考核仍按原逻辑过滤
+- **WHEN** CV 方向考生查询考核时间列表，且存在 `direction = STRUCTURAL_DESIGN` 的考核
+- **THEN** 系统 SHALL NOT 返回该考核时间
+
+## MODIFIED Requirements
+
+### Requirement: 分页查询考核时间（管理端）
+系统 SHALL 提供管理员分页查询接口 `GET /api/v1/admin/assessment-times`，支持 `page`（默认 0）和 `size`（默认 5）参数。
+
+查询结果 SHALL 根据当前用户角色过滤：
+- CANDIDATE：只返回当前用户方向 + 当前用户入学年份的考核时间，以及 `direction IS NULL` 且 `grade` 匹配的跨方向考核
+- MEMBER：返回当前用户方向的全部考核时间，以及 `direction IS NULL` 的跨方向考核
+- DIRECTION_ADMIN 及以上：返回全部考核时间
+
+#### Scenario: 方向管理员查看全部考核时间
+- **WHEN** DIRECTION_ADMIN 角色用户请求分页查询
+- **THEN** 系统 SHALL 返回所有方向的考核时间，不按方向或年级过滤
+
+#### Scenario: 团队成员查看自己方向的考核时间
+- **WHEN** MEMBER 角色用户请求分页查询
+- **THEN** 系统 SHALL 只返回该用户方向的全部考核时间（不限年级），以及 `direction IS NULL` 的跨方向考核
+
+#### Scenario: 考生查看自己方向和入学年份的考核时间
+- **WHEN** CANDIDATE 角色用户（学号=2024xxx）请求分页查询
+- **THEN** 系统 SHALL 只返回该用户方向 + grade=2024 的考核时间，以及 `direction IS NULL` 且 `grade = 2024` 的跨方向考核
+
+### Requirement: 考核时间数据模型包含年级字段
+系统 SHALL 在 `tb_assessment_time` 表中包含 `grade` 字段（INTEGER, NOT NULL），取值为入学年份（如 2024、2025）。`(direction, epoch, grade)` 组合 SHALL 具有唯一约束，其中 `direction` 为 `null` 时按 `null` 值参与唯一约束。
+
+#### Scenario: 唯一约束生效（含跨方向）
+- **WHEN** 尝试创建 direction=null, epoch=1, grade=2024 的考核时间，且该组合已存在
+- **THEN** 系统 SHALL 返回 400 错误，提示该方向轮次年级的考核时间已存在
+
+#### Scenario: 跨方向和普通方向不冲突
+- **WHEN** 已存在 direction=null, epoch=1, grade=2024 的考核，再创建 direction=COMPUTER_VISION, epoch=1, grade=2024 的考核
+- **THEN** 系统 SHALL 允许创建成功
diff --git a/openspec/changes/assessment-team-support/specs/frontend-assessment-question-page/spec.md b/openspec/changes/assessment-team-support/specs/frontend-assessment-question-page/spec.md
new file mode 100644
index 0000000..1c0bbfb
--- /dev/null
+++ b/openspec/changes/assessment-team-support/specs/frontend-assessment-question-page/spec.md
@@ -0,0 +1,59 @@
+## ADDED Requirements
+
+### Requirement: FILE_UPLOAD 题在组队考核中展示组队前置流程
+在允许组队的考核中，FILE_UPLOAD 类型的题目 SHALL 在考题目录页和题目详情页展示组队相关状态。未组队的用户 SHALL 看到创建/加入队伍的入口，已组队的用户 SHALL 看到队伍信息面板。
+
+#### Scenario: 未组队用户查看 FILE_UPLOAD 题
+- **WHEN** 未组队的用户进入允许组队的考核的考题目录页
+- **THEN** FILE_UPLOAD 题 SHALL 显示"创建队伍"或"加入队伍"按钮，点击后进入组队流程
+
+#### Scenario: 已组队用户查看 FILE_UPLOAD 题
+- **WHEN** 已组队的用户进入允许组队的考核的考题目录页
+- **THEN** FILE_UPLOAD 题 SHALL 显示队伍名称和当前成员数
+
+#### Scenario: 非 FILE_UPLOAD 题不受组队影响
+- **WHEN** 用户查看单选题、多选题或算法题
+- **THEN** 页面 SHALL 正常展示个人答题界面，不显示组队相关 UI
+
+### Requirement: 邀请码输入与预览确认
+用户 SHALL 通过输入邀请码预览队伍信息，确认后再加入。预览 SHALL 展示队伍名称、队长信息、成员列表（含方向）。
+
+成员列表 SHALL 使用现有的用户信息展示组件，复用 `UserInfo` 数据结构。
+
+#### Scenario: 输入邀请码预览队伍
+- **WHEN** 用户在加入队伍弹窗中输入邀请码并点击预览
+- **THEN** 系统 SHALL 调用预览接口并展示队伍名称、队长、成员列表（含各成员方向）
+
+#### Scenario: 确认加入队伍
+- **WHEN** 用户预览队伍信息后点击确认加入
+- **THEN** 系统 SHALL 调用加入接口，成功后刷新页面并展示队伍信息
+
+#### Scenario: 取消加入队伍
+- **WHEN** 用户预览队伍信息后点击取消
+- **THEN** 系统 SHALL 关闭弹窗，不调用加入接口
+
+### Requirement: 队长上传区与队员只读区
+FILE_UPLOAD 题的题目详情页 SHALL 根据当前用户是否为队长展示不同的操作区。
+
+队长 SHALL 看到文件上传组件和提交按钮。队员 SHALL 看到"队长已提交"的文件列表，并显示"您无上传权限，请联系队长"的提示。
+
+#### Scenario: 队长进入 FILE_UPLOAD 题
+- **WHEN** 队长进入 FILE_UPLOAD 题详情页
+- **THEN** 页面 SHALL 展示文件上传组件、已上传文件列表、提交/更新按钮
+
+#### Scenario: 队员进入 FILE_UPLOAD 题
+- **WHEN** 队员进入 FILE_UPLOAD 题详情页
+- **THEN** 页面 SHALL 展示队长已提交的文件列表，不展示上传组件和提交按钮，并显示无权限提示
+
+#### Scenario: 队员查看队长更新的文件
+- **WHEN** 队长更新提交的文件后，队员刷新页面
+- **THEN** 队员 SHALL 看到最新的文件列表
+
+### Requirement: 题目页展示队伍信息面板
+FILE_UPLOAD 题的题目详情页 SHALL 在题目描述区域附近展示队伍信息面板，包含队伍名称、队长、成员列表及各自方向。
+
+成员信息 SHALL 复用现有的用户展示组件。
+
+#### Scenario: 队伍信息面板展示
+- **WHEN** 已组队的用户进入 FILE_UPLOAD 题详情页
+- **THEN** 页面 SHALL 展示队伍信息面板，包含队伍名称、队长姓名、成员列表（含方向标签）
diff --git a/openspec/changes/assessment-team-support/tasks.md b/openspec/changes/assessment-team-support/tasks.md
new file mode 100644
index 0000000..7f453ff
--- /dev/null
+++ b/openspec/changes/assessment-team-support/tasks.md
@@ -0,0 +1,103 @@
+## 1. Database Migration
+
+- [x] 1.1 Create Flyway migration: add `allow_team` to `tb_assessment_time`, add `team_id` to `tb_assessment_answer`
+- [x] 1.2 Create Flyway migration: create `tb_assessment_team` and `tb_assessment_team_member` tables
+
+## 2. Domain Layer (Backend)
+
+- [x] 2.1 Add `allowTeam` field to `AssessmentTime` entity with create/update behavior
+- [x] 2.2 Add `teamId` field to `AssessmentAnswer` entity
+- [x] 2.3 Create `AssessmentTeam` domain entity with fields: id, assessmentTimeId, leaderId, name, inviteCode, status
+- [x] 2.4 Create `AssessmentTeamMember` domain entity/value object
+- [x] 2.5 Create `AssessmentTeamRepository` interface with methods: save, findById, findByAssessmentTimeIdAndUserId, findByInviteCode, delete, updateLeader, addMember, removeMember
+
+## 3. Application Layer (Backend)
+
+- [ ] 3.1 Create `AssessmentTeamAppService` interface with methods: createTeam, previewTeam, joinTeam, getMyTeam, leaveTeam, transferLeader, disbandTeam
+- [ ] 3.2 Implement `AssessmentTeamAppServiceImpl.createTeam` with invite code generation and leader assignment
+- [ ] 3.3 Implement `AssessmentTeamAppServiceImpl.previewTeam` (side-effect free preview by invite code)
+- [ ] 3.4 Implement `AssessmentTeamAppServiceImpl.joinTeam` with validation (not in other team, no personal answer, time not ended)
+- [ ] 3.5 Implement `AssessmentTeamAppServiceImpl.getMyTeam` returning team info with member list (reuse UserInfo)
+- [ ] 3.6 Implement `AssessmentTeamAppServiceImpl.leaveTeam` (leader cannot leave without transfer)
+- [ ] 3.7 Implement `AssessmentTeamAppServiceImpl.transferLeader` (validate target is team member)
+- [ ] 3.8 Implement `AssessmentTeamAppServiceImpl.disbandTeam` (leader only)
+- [ ] 3.9 Modify `AssessmentTimeAppServiceImpl.listAssessmentTimesForUser` to include `direction IS NULL` results
+- [ ] 3.10 Modify `AssessmentTimeAppServiceImpl.createAssessmentTime` to accept and save `allowTeam`
+- [ ] 3.11 Modify `AssessmentTimeAppServiceImpl.updateAssessmentTime` to accept and update `allowTeam`
+- [ ] 3.12 Modify `AssessmentAnswerAppServiceImpl.createAnswer` to validate team/leader permission for FILE_UPLOAD in team-enabled assessments
+- [ ] 3.13 Modify `AssessmentAnswerAppServiceImpl.updateAnswer` to validate team/leader permission for FILE_UPLOAD in team-enabled assessments
+- [ ] 3.14 Modify `AssessmentAnswerAppServiceImpl.getMyAnswer` to return leader's answer for team members on FILE_UPLOAD questions
+- [ ] 3.15 Modify `AssessmentAnswerAppServiceImpl.validateDirectionMatch` to allow `time.direction == null` (cross-direction)
+
+## 4. Infrastructure Layer (Backend)
+
+- [x] 4.1 Create `AssessmentTeamDO` and `AssessmentTeamMemberDO` data objects
+- [x] 4.2 Create `AssessmentTeamMapper` interface and XML with CRUD operations
+- [x] 4.3 Create `AssessmentTeamMemberMapper` interface and XML
+- [x] 4.4 Implement `AssessmentTeamRepositoryImpl` with DO conversion
+- [x] 4.5 Create repository converters for team entities
+- [x] 4.6 Modify `AssessmentTimeMapper.xml` `selectPageByUserParticipation` to support `direction IS NULL`
+- [x] 4.7 Modify `AssessmentAnswerMapper.xml` to support `team_id` field
+
+## 5. API Layer (Backend)
+
+- [ ] 5.1 Create `AssessmentTeamController` with endpoints: POST /api/v1/assessment-teams, POST /api/v1/assessment-teams/preview, POST /api/v1/assessment-teams/join, GET /api/v1/assessment-teams/my-team, POST /api/v1/assessment-teams/leave, POST /api/v1/assessment-teams/transfer, DELETE /api/v1/assessment-teams/{id}
+- [ ] 5.2 Create `AssessmentTeamDTO`, `CreateTeamRequestDTO`, `JoinTeamRequestDTO`, `PreviewTeamRequestDTO`, `TeamMemberDTO` (reuse UserInfo fields)
+- [ ] 5.3 Create request/response converters for team DTOs
+- [ ] 5.4 Add `@RequiresPermission` annotations to all team endpoints with proper `value` ensuring global uniqueness
+- [ ] 5.5 Modify `AdminAssessmentTimeController` create/update endpoints to accept `allowTeam` field
+- [ ] 5.6 Modify `AssessmentTimeDTO` to include `allowTeam` field
+- [ ] 5.7 Modify `AssessmentAnswerController` if needed for team-related answer queries
+
+## 6. Frontend - Admin
+
+- [ ] 6.1 Update `AssessmentTimeDrawer.tsx` to add "允许组队" switch
+- [ ] 6.2 Update admin assessment time list to display "允许组队" status
+- [ ] 6.3 Update assessment time form validation to handle `allowTeam`
+
+## 7. Frontend - User Assessment List
+
+- [ ] 7.1 Update `AssessmentCard` component to show team-enabled indicator
+- [ ] 7.1 Verify cross-direction assessments (`direction = null`) display correctly in assessment list
+
+## 8. Frontend - Question List Page
+
+- [ ] 8.1 Add team status query on `/assessment/{timeId}/questions` page (call getMyTeam on load)
+- [ ] 8.2 For FILE_UPLOAD questions in team-enabled assessments: show "创建队伍" or "加入队伍" button when not in team
+- [ ] 8.3 For FILE_UPLOAD questions in team-enabled assessments: show team name and member count when already in team
+- [ ] 8.4 Non-FILE_UPLOAD questions remain unchanged regardless of team settings
+
+## 9. Frontend - Question Detail Page (FILE_UPLOAD)
+
+- [ ] 9.1 Add team info panel showing team name, leader, members with direction badges
+- [ ] 9.2 Add invite code display with copy-to-clipboard button (visible to leader)
+- [ ] 9.3 Add "加入队伍" modal with invite code input and preview confirmation flow
+- [ ] 9.4 Leader view: show file upload component, submit/update buttons
+- [ ] 9.5 Member view: show leader-submitted files as read-only list with "no permission" message
+- [ ] 9.6 Reuse existing UserInfo display components for member list
+
+## 10. Frontend - Team Management
+
+- [ ] 10.1 Add "退出队伍" button for members (with confirmation)
+- [ ] 10.2 Add "转让队长" dialog for leader (select from members)
+- [ ] 10.3 Add "解散队伍" button for leader (with confirmation)
+
+## 11. Testing
+
+- [ ] 11.1 Write unit tests for `AssessmentTeamAppServiceImpl` (create, join, leave, transfer, preview)
+- [ ] 11.2 Write unit tests for team permission validation in `AssessmentAnswerAppServiceImpl`
+- [ ] 11.3 Write unit tests for cross-direction query in `AssessmentTimeAppServiceImpl`
+- [ ] 11.4 Write integration tests for `AssessmentTeamController` endpoints
+- [ ] 11.5 Write repository tests for `AssessmentTeamRepositoryImpl`
+- [ ] 11.6 Run full backend test suite to verify no regressions
+
+## 12. E2E Verification
+
+- [ ] 12.1 Build and deploy backend Docker image
+- [ ] 12.2 Create cross-direction assessment with `allowTeam = true`
+- [ ] 12.3 Create FILE_UPLOAD question in the assessment
+- [ ] 12.4 End-to-end test: User A (CV) creates team, User B (电控) joins via invite code with preview confirmation
+- [ ] 12.5 End-to-end test: Leader submits file, member views the file
+- [ ] 12.6 End-to-end test: Non-team user cannot access FILE_UPLOAD question in team-enabled assessment
+- [ ] 12.7 End-to-end test: Judge scores each team member independently
+
diff --git a/src/backend/src/main/java/com/bluenet/web/api/controller/v1/AssessmentTeamController.java b/src/backend/src/main/java/com/bluenet/web/api/controller/v1/AssessmentTeamController.java
new file mode 100644
index 0000000..d0a550b
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/controller/v1/AssessmentTeamController.java
@@ -0,0 +1,173 @@
+package com.bluenet.web.api.controller.v1;
+
+import com.bluenet.web.api.converter.assessment_team.AssessmentTeamResponseConverter;
+import com.bluenet.web.api.dto.ResponseMessage;
+import com.bluenet.web.api.dto.assessment_team.*;
+import com.bluenet.web.application.TeamPreviewResult;
+import com.bluenet.web.application.TeamResult;
+import com.bluenet.web.application.service.AssessmentTeamAppService;
+import com.bluenet.web.domain.model.vo.UserVO;
+import com.bluenet.web.infrastructure.security.annotation.AccessLevel;
+import com.bluenet.web.infrastructure.security.annotation.RequiresPermission;
+import com.bluenet.web.infrastructure.security.util.UserCTX;
+import io.swagger.v3.oas.annotations.Operation;
+import io.swagger.v3.oas.annotations.Parameter;
+import io.swagger.v3.oas.annotations.media.Content;
+import io.swagger.v3.oas.annotations.media.Schema;
+import io.swagger.v3.oas.annotations.responses.ApiResponse;
+import io.swagger.v3.oas.annotations.responses.ApiResponses;
+import io.swagger.v3.oas.annotations.security.SecurityRequirement;
+import io.swagger.v3.oas.annotations.tags.Tag;
+import jakarta.validation.Valid;
+import lombok.RequiredArgsConstructor;
+import org.springframework.web.bind.annotation.*;
+
+/**
+ * 考核队伍控制器
+ * <p>
+ * 提供考核队伍的创建、加入、查询、管理等接口
+ * </p>
+ */
+@Tag(name = "考核队伍", description = "考核队伍管理接口，已登录用户可访问")
+@RestController
+@RequestMapping("/api/v1/assessment-teams")
+@RequiredArgsConstructor
+@SecurityRequirement(name = "bearer-jwt")
+public class AssessmentTeamController {
+
+    private final AssessmentTeamAppService assessmentTeamAppService;
+    private final AssessmentTeamResponseConverter responseConverter;
+
+    @Operation(summary = "创建队伍", description = "为指定考核时间创建一个新的队伍，当前用户自动成为队长")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "创建成功", content = @Content(mediaType = "application/json", schema = @Schema(implementation = AssessmentTeamDTO.class))),
+            @ApiResponse(responseCode = "400", description = "该考核不允许组队、已加入队伍或已提交个人答案", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "创建队伍", value = "assessment-team:create", access = AccessLevel.AUTHENTICATED)
+    @PostMapping
+    public ResponseMessage<AssessmentTeamDTO> createTeam(
+            @Valid @RequestBody CreateTeamRequestDTO request) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        TeamResult result = assessmentTeamAppService.createTeam(request.getAssessmentTimeId(), request.getName());
+        return ResponseMessage.success(responseConverter.toDTO(result));
+    }
+
+    @Operation(summary = "预览队伍", description = "通过邀请码预览队伍信息，无需登录也可查看")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "查询成功", content = @Content(mediaType = "application/json", schema = @Schema(implementation = TeamPreviewResponseDTO.class))),
+            @ApiResponse(responseCode = "400", description = "邀请码无效或考核已结束", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "预览队伍", value = "assessment-team:preview", access = AccessLevel.AUTHENTICATED)
+    @PostMapping("/preview")
+    public ResponseMessage<TeamPreviewResponseDTO> previewTeam(
+            @Valid @RequestBody PreviewTeamRequestDTO request) {
+        TeamPreviewResult result = assessmentTeamAppService.previewTeam(request.getInviteCode());
+        return ResponseMessage.success(toPreviewDTO(result));
+    }
+
+    @Operation(summary = "加入队伍", description = "通过邀请码加入指定队伍")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "加入成功", content = @Content(mediaType = "application/json", schema = @Schema(implementation = AssessmentTeamDTO.class))),
+            @ApiResponse(responseCode = "400", description = "邀请码无效、已加入队伍、已提交个人答案或考核已结束", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "加入队伍", value = "assessment-team:join", access = AccessLevel.AUTHENTICATED)
+    @PostMapping("/join")
+    public ResponseMessage<AssessmentTeamDTO> joinTeam(
+            @Valid @RequestBody JoinTeamRequestDTO request) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        TeamResult result = assessmentTeamAppService.joinTeam(request.getInviteCode());
+        return ResponseMessage.success(responseConverter.toDTO(result));
+    }
+
+    @Operation(summary = "查询我的队伍", description = "查询当前用户在指定考核时间下的队伍信息")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "查询成功", content = @Content(mediaType = "application/json", schema = @Schema(implementation = AssessmentTeamDTO.class))),
+            @ApiResponse(responseCode = "404", description = "未加入队伍", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "查询我的队伍", value = "assessment-team:query-my-team", access = AccessLevel.AUTHENTICATED)
+    @GetMapping("/my-team")
+    public ResponseMessage<AssessmentTeamDTO> getMyTeam(
+            @Parameter(description = "考核时间ID", required = true) @RequestParam Long assessmentTimeId) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        TeamResult result = assessmentTeamAppService.getMyTeam(assessmentTimeId);
+        if (result == null) {
+            return ResponseMessage.error(404, "未加入队伍");
+        }
+        return ResponseMessage.success(responseConverter.toDTO(result));
+    }
+
+    @Operation(summary = "离开队伍", description = "离开当前所在的队伍（队长不能离开）")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "离开成功"),
+            @ApiResponse(responseCode = "400", description = "不是队伍成员", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class))),
+            @ApiResponse(responseCode = "403", description = "队长不能离开队伍", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "离开队伍", value = "assessment-team:leave", access = AccessLevel.AUTHENTICATED)
+    @PostMapping("/leave")
+    public ResponseMessage<Void> leaveTeam(
+            @Valid @RequestBody LeaveTeamRequestDTO request) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        assessmentTeamAppService.leaveTeam(request.getTeamId());
+        return ResponseMessage.success();
+    }
+
+    @Operation(summary = "转让队长", description = "将队长权限转让给队伍中的另一名成员")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "转让成功", content = @Content(mediaType = "application/json", schema = @Schema(implementation = AssessmentTeamDTO.class))),
+            @ApiResponse(responseCode = "400", description = "新队长不是队伍成员", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class))),
+            @ApiResponse(responseCode = "403", description = "只有队长可以转让队长", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "转让队长", value = "assessment-team:transfer", access = AccessLevel.AUTHENTICATED)
+    @PostMapping("/transfer")
+    public ResponseMessage<AssessmentTeamDTO> transferLeader(
+            @Valid @RequestBody TransferLeaderRequestDTO request) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        TeamResult result = assessmentTeamAppService.transferLeader(request.getTeamId(), request.getNewLeaderId());
+        return ResponseMessage.success(responseConverter.toDTO(result));
+    }
+
+    @Operation(summary = "解散队伍", description = "解散当前队伍（仅队长可操作）")
+    @ApiResponses({
+            @ApiResponse(responseCode = "200", description = "解散成功"),
+            @ApiResponse(responseCode = "403", description = "只有队长可以解散队伍", content = @Content(mediaType = "application/json", schema = @Schema(implementation = ResponseMessage.class)))
+    })
+    @RequiresPermission(name = "解散队伍", value = "assessment-team:disband", access = AccessLevel.AUTHENTICATED)
+    @DeleteMapping("/{id}")
+    public ResponseMessage<Void> disbandTeam(
+            @Parameter(description = "队伍ID", required = true) @PathVariable Long id) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+        assessmentTeamAppService.disbandTeam(id);
+        return ResponseMessage.success();
+    }
+
+    private TeamPreviewResponseDTO toPreviewDTO(TeamPreviewResult result) {
+        return TeamPreviewResponseDTO.builder()
+                .id(result.id())
+                .assessmentTimeId(result.assessmentTimeId())
+                .leaderUsername(result.leaderUsername())
+                .name(result.name())
+                .status(result.status())
+                .createdAt(result.createdAt())
+                .memberCount(result.memberCount())
+                .memberUsernames(result.memberUsernames())
+                .build();
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_team/AssessmentTeamResponseConverter.java b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_team/AssessmentTeamResponseConverter.java
new file mode 100644
index 0000000..9e1be8b
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_team/AssessmentTeamResponseConverter.java
@@ -0,0 +1,59 @@
+package com.bluenet.web.api.converter.assessment_team;
+
+import com.bluenet.web.api.dto.assessment_team.AssessmentTeamDTO;
+import com.bluenet.web.api.dto.assessment_team.TeamMemberDTO;
+import com.bluenet.web.application.TeamResult;
+import org.springframework.stereotype.Component;
+
+import java.util.Collections;
+import java.util.List;
+
+/**
+ * 考核队伍响应转换器
+ * <p>
+ * 负责将应用层结果转换为 API 响应 DTO
+ * </p>
+ */
+@Component
+public class AssessmentTeamResponseConverter {
+
+    /**
+     * 将应用层队伍结果转换为 DTO
+     */
+    public AssessmentTeamDTO toDTO(TeamResult result) {
+        if (result == null) {
+            return null;
+        }
+        return AssessmentTeamDTO.builder()
+                .id(result.id())
+                .assessmentTimeId(result.assessmentTimeId())
+                .leaderId(result.leaderId())
+                .name(result.name())
+                .inviteCode(result.inviteCode())
+                .status(result.status())
+                .createdAt(result.createdAt())
+                .members(toMemberDTOs(result.members()))
+                .build();
+    }
+
+    private List<TeamMemberDTO> toMemberDTOs(List<TeamResult.TeamMemberResult> members) {
+        if (members == null || members.isEmpty()) {
+            return Collections.emptyList();
+        }
+        return members.stream()
+                .map(this::toMemberDTO)
+                .toList();
+    }
+
+    private TeamMemberDTO toMemberDTO(TeamResult.TeamMemberResult member) {
+        return TeamMemberDTO.builder()
+                .id(member.id())
+                .userId(member.userId())
+                .username(member.username())
+                .direction(member.direction())
+                .avatarFileId(member.avatarFileId())
+                .joinedAt(member.joinedAt())
+                .leader(member.isLeader())
+                .build();
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeRequestConverter.java b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeRequestConverter.java
index a1ecc73..6f86fc0 100644
--- a/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeRequestConverter.java
+++ b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeRequestConverter.java
@@ -25,7 +25,8 @@ public class AssessmentTimeRequestConverter {
                 dto.getStartTime(),
                 dto.getEndTime(),
                 dto.getTimeLimit(),
-                Boolean.TRUE.equals(dto.getTimeLimit()) ? dto.getTimeLimitMinutes() : null);
+                Boolean.TRUE.equals(dto.getTimeLimit()) ? dto.getTimeLimitMinutes() : null,
+                dto.getAllowTeam());
     }
 
     /**
@@ -40,6 +41,7 @@ public class AssessmentTimeRequestConverter {
                 dto.getStartTime(),
                 dto.getEndTime(),
                 dto.getTimeLimit(),
-                Boolean.FALSE.equals(dto.getTimeLimit()) ? null : dto.getTimeLimitMinutes());
+                Boolean.FALSE.equals(dto.getTimeLimit()) ? null : dto.getTimeLimitMinutes(),
+                dto.getAllowTeam());
     }
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeResponseConverter.java b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeResponseConverter.java
index 99d0662..e36b471 100644
--- a/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeResponseConverter.java
+++ b/src/backend/src/main/java/com/bluenet/web/api/converter/assessment_time/AssessmentTimeResponseConverter.java
@@ -50,6 +50,7 @@ public class AssessmentTimeResponseConverter {
                 .timeLimitMinutes(result.timeLimitMinutes())
                 .totalQuestions(result.totalQuestions())
                 .completedQuestions(result.completedQuestions())
+                .allowTeam(result.allowTeam())
                 .build();
     }
 
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/AssessmentTeamDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/AssessmentTeamDTO.java
new file mode 100644
index 0000000..c7fbce4
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/AssessmentTeamDTO.java
@@ -0,0 +1,48 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import io.swagger.v3.oas.annotations.media.Schema;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+import java.time.LocalDateTime;
+import java.util.List;
+
+/**
+ * 考核队伍数据传输对象
+ * <p>
+ * 用于API响应中返回队伍信息
+ * </p>
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "考核队伍信息")
+public class AssessmentTeamDTO {
+    @Schema(description = "队伍ID")
+    private Long id;
+
+    @Schema(description = "考核时间ID")
+    private Long assessmentTimeId;
+
+    @Schema(description = "队长ID")
+    private Long leaderId;
+
+    @Schema(description = "队伍名称")
+    private String name;
+
+    @Schema(description = "邀请码")
+    private String inviteCode;
+
+    @Schema(description = "队伍状态")
+    private AssessmentTeam.TeamStatus status;
+
+    @Schema(description = "创建时间")
+    private LocalDateTime createdAt;
+
+    @Schema(description = "成员列表")
+    private List<TeamMemberDTO> members;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/CreateTeamRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/CreateTeamRequestDTO.java
new file mode 100644
index 0000000..648e1eb
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/CreateTeamRequestDTO.java
@@ -0,0 +1,27 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import jakarta.validation.constraints.NotBlank;
+import jakarta.validation.constraints.NotNull;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * 创建队伍请求DTO
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "创建队伍请求")
+public class CreateTeamRequestDTO {
+    @NotNull(message = "考核时间ID不能为空")
+    @Schema(description = "考核时间ID", required = true)
+    private Long assessmentTimeId;
+
+    @NotBlank(message = "队伍名称不能为空")
+    @Schema(description = "队伍名称", required = true)
+    private String name;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/JoinTeamRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/JoinTeamRequestDTO.java
new file mode 100644
index 0000000..0330de9
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/JoinTeamRequestDTO.java
@@ -0,0 +1,22 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import jakarta.validation.constraints.NotBlank;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * 加入队伍请求DTO
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "加入队伍请求")
+public class JoinTeamRequestDTO {
+    @NotBlank(message = "邀请码不能为空")
+    @Schema(description = "邀请码", required = true)
+    private String inviteCode;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/LeaveTeamRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/LeaveTeamRequestDTO.java
new file mode 100644
index 0000000..016e699
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/LeaveTeamRequestDTO.java
@@ -0,0 +1,22 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import jakarta.validation.constraints.NotNull;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * 离开队伍请求DTO
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "离开队伍请求")
+public class LeaveTeamRequestDTO {
+    @NotNull(message = "队伍ID不能为空")
+    @Schema(description = "队伍ID", required = true)
+    private Long teamId;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/PreviewTeamRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/PreviewTeamRequestDTO.java
new file mode 100644
index 0000000..72fafcc
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/PreviewTeamRequestDTO.java
@@ -0,0 +1,22 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import jakarta.validation.constraints.NotBlank;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * 预览队伍请求DTO
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "预览队伍请求")
+public class PreviewTeamRequestDTO {
+    @NotBlank(message = "邀请码不能为空")
+    @Schema(description = "邀请码", required = true)
+    private String inviteCode;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamMemberDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamMemberDTO.java
new file mode 100644
index 0000000..3dbbe03
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamMemberDTO.java
@@ -0,0 +1,43 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+import java.time.LocalDateTime;
+
+/**
+ * 队伍成员数据传输对象
+ * <p>
+ * 用于API响应中返回队伍成员信息
+ * </p>
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "队伍成员信息")
+public class TeamMemberDTO {
+    @Schema(description = "成员记录ID")
+    private Long id;
+
+    @Schema(description = "用户ID")
+    private Long userId;
+
+    @Schema(description = "用户名")
+    private String username;
+
+    @Schema(description = "方向")
+    private String direction;
+
+    @Schema(description = "头像文件ID")
+    private Long avatarFileId;
+
+    @Schema(description = "加入时间")
+    private LocalDateTime joinedAt;
+
+    @Schema(description = "是否为队长")
+    private boolean leader;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamPreviewResponseDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamPreviewResponseDTO.java
new file mode 100644
index 0000000..17bc09b
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TeamPreviewResponseDTO.java
@@ -0,0 +1,48 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import io.swagger.v3.oas.annotations.media.Schema;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+import java.time.LocalDateTime;
+import java.util.List;
+
+/**
+ * 队伍预览响应DTO
+ * <p>
+ * 用于通过邀请码预览队伍信息的响应
+ * </p>
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "队伍预览信息")
+public class TeamPreviewResponseDTO {
+    @Schema(description = "队伍ID")
+    private Long id;
+
+    @Schema(description = "考核时间ID")
+    private Long assessmentTimeId;
+
+    @Schema(description = "队长用户名")
+    private String leaderUsername;
+
+    @Schema(description = "队伍名称")
+    private String name;
+
+    @Schema(description = "队伍状态")
+    private AssessmentTeam.TeamStatus status;
+
+    @Schema(description = "创建时间")
+    private LocalDateTime createdAt;
+
+    @Schema(description = "当前成员数量")
+    private int memberCount;
+
+    @Schema(description = "成员用户名列表")
+    private List<String> memberUsernames;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TransferLeaderRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TransferLeaderRequestDTO.java
new file mode 100644
index 0000000..3d3c36c
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_team/TransferLeaderRequestDTO.java
@@ -0,0 +1,26 @@
+package com.bluenet.web.api.dto.assessment_team;
+
+import io.swagger.v3.oas.annotations.media.Schema;
+import jakarta.validation.constraints.NotNull;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * 转让队长请求DTO
+ */
+@Data
+@AllArgsConstructor
+@NoArgsConstructor
+@Builder
+@Schema(description = "转让队长请求")
+public class TransferLeaderRequestDTO {
+    @NotNull(message = "队伍ID不能为空")
+    @Schema(description = "队伍ID", required = true)
+    private Long teamId;
+
+    @NotNull(message = "新队长用户ID不能为空")
+    @Schema(description = "新队长用户ID", required = true)
+    private Long newLeaderId;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/AssessmentTimeDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/AssessmentTimeDTO.java
index bb7ffcb..6b261e1 100644
--- a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/AssessmentTimeDTO.java
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/AssessmentTimeDTO.java
@@ -50,4 +50,7 @@ public class AssessmentTimeDTO {
 
     @Schema(description = "已完成题目数")
     private Integer completedQuestions;
+
+    @Schema(description = "是否允许组队")
+    private Boolean allowTeam;
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/CreateAssessmentTimeRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/CreateAssessmentTimeRequestDTO.java
index 57defee..4c61833 100644
--- a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/CreateAssessmentTimeRequestDTO.java
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/CreateAssessmentTimeRequestDTO.java
@@ -48,4 +48,7 @@ public class CreateAssessmentTimeRequestDTO {
 
     @Schema(description = "限时分钟数（timeLimit为true时必填）")
     private Integer timeLimitMinutes;
+
+    @Schema(description = "是否允许组队")
+    private Boolean allowTeam;
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/UpdateAssessmentTimeRequestDTO.java b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/UpdateAssessmentTimeRequestDTO.java
index 02403c7..acc460e 100644
--- a/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/UpdateAssessmentTimeRequestDTO.java
+++ b/src/backend/src/main/java/com/bluenet/web/api/dto/assessment_time/UpdateAssessmentTimeRequestDTO.java
@@ -41,4 +41,7 @@ public class UpdateAssessmentTimeRequestDTO {
 
     @Schema(description = "限时分钟数")
     private Integer timeLimitMinutes;
+
+    @Schema(description = "是否允许组队")
+    private Boolean allowTeam;
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/application/AssessmentTimeResult.java b/src/backend/src/main/java/com/bluenet/web/application/AssessmentTimeResult.java
index c9d4669..c767f66 100644
--- a/src/backend/src/main/java/com/bluenet/web/application/AssessmentTimeResult.java
+++ b/src/backend/src/main/java/com/bluenet/web/application/AssessmentTimeResult.java
@@ -27,6 +27,8 @@ public record AssessmentTimeResult(
         Boolean timeLimit,
         /** 限时分钟数 */
         Integer timeLimitMinutes,
+        /** 是否允许组队 */
+        Boolean allowTeam,
         /** 题目总数 */
         Integer totalQuestions,
         /** 已完成题目数 */
diff --git a/src/backend/src/main/java/com/bluenet/web/application/TeamPreviewResult.java b/src/backend/src/main/java/com/bluenet/web/application/TeamPreviewResult.java
new file mode 100644
index 0000000..5abac51
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/application/TeamPreviewResult.java
@@ -0,0 +1,31 @@
+package com.bluenet.web.application;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+
+import java.time.LocalDateTime;
+import java.util.List;
+
+/**
+ * 考核队伍预览应用层结果对象。
+ * <p>
+ * 封装了通过邀请码预览队伍信息返回给 API 层的数据。
+ * </p>
+ */
+public record TeamPreviewResult(
+        /** 队伍ID */
+        Long id,
+        /** 考核时间ID */
+        Long assessmentTimeId,
+        /** 队长用户名 */
+        String leaderUsername,
+        /** 队伍名称 */
+        String name,
+        /** 队伍状态 */
+        AssessmentTeam.TeamStatus status,
+        /** 创建时间 */
+        LocalDateTime createdAt,
+        /** 当前成员数量 */
+        int memberCount,
+        /** 成员列表（仅包含用户名） */
+        List<String> memberUsernames) {
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/application/TeamResult.java b/src/backend/src/main/java/com/bluenet/web/application/TeamResult.java
new file mode 100644
index 0000000..0fa8a74
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/application/TeamResult.java
@@ -0,0 +1,51 @@
+package com.bluenet.web.application;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+
+import java.time.LocalDateTime;
+import java.util.List;
+
+/**
+ * 考核队伍应用层结果对象。
+ * <p>
+ * 封装了考核队伍相关操作返回给 API 层的数据。
+ * </p>
+ */
+public record TeamResult(
+        /** 队伍ID */
+        Long id,
+        /** 考核时间ID */
+        Long assessmentTimeId,
+        /** 队长ID */
+        Long leaderId,
+        /** 队伍名称 */
+        String name,
+        /** 邀请码 */
+        String inviteCode,
+        /** 队伍状态 */
+        AssessmentTeam.TeamStatus status,
+        /** 创建时间 */
+        LocalDateTime createdAt,
+        /** 成员列表 */
+        List<TeamMemberResult> members) {
+
+    /**
+     * 队伍成员结果对象。
+     */
+    public record TeamMemberResult(
+            /** 成员ID */
+            Long id,
+            /** 用户ID */
+            Long userId,
+            /** 用户名 */
+            String username,
+            /** 方向 */
+            String direction,
+            /** 头像文件ID */
+            Long avatarFileId,
+            /** 加入时间 */
+            LocalDateTime joinedAt,
+            /** 是否为队长 */
+            boolean isLeader) {
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/application/command/assessment_time/AssessmentTimeCommands.java b/src/backend/src/main/java/com/bluenet/web/application/command/assessment_time/AssessmentTimeCommands.java
index bf5f2c1..672417b 100644
--- a/src/backend/src/main/java/com/bluenet/web/application/command/assessment_time/AssessmentTimeCommands.java
+++ b/src/backend/src/main/java/com/bluenet/web/application/command/assessment_time/AssessmentTimeCommands.java
@@ -36,7 +36,9 @@ public class AssessmentTimeCommands {
             /** 是否限时 */
             Boolean timeLimit,
             /** 限时分钟数 */
-            Integer timeLimitMinutes) {
+            Integer timeLimitMinutes,
+            /** 是否允许组队 */
+            Boolean allowTeam) {
     }
 
     /**
@@ -61,6 +63,8 @@ public class AssessmentTimeCommands {
             /** 是否限时 */
             Boolean timeLimit,
             /** 限时分钟数 */
-            Integer timeLimitMinutes) {
+            Integer timeLimitMinutes,
+            /** 是否允许组队 */
+            Boolean allowTeam) {
     }
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/application/service/AssessmentTeamAppService.java b/src/backend/src/main/java/com/bluenet/web/application/service/AssessmentTeamAppService.java
new file mode 100644
index 0000000..b2f36cb
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/application/service/AssessmentTeamAppService.java
@@ -0,0 +1,78 @@
+package com.bluenet.web.application.service;
+
+import com.bluenet.web.application.TeamPreviewResult;
+import com.bluenet.web.application.TeamResult;
+
+/**
+ * 考核队伍应用服务接口。
+ * <p>
+ * 定义了考核队伍聚合在应用层的所有业务操作。
+ * </p>
+ */
+public interface AssessmentTeamAppService {
+
+    /**
+     * 创建队伍。
+     *
+     * @param assessmentTimeId
+     *            考核时间ID
+     * @param name
+     *            队伍名称
+     * @return 创建后的队伍结果
+     */
+    TeamResult createTeam(Long assessmentTimeId, String name);
+
+    /**
+     * 通过邀请码预览队伍信息。
+     *
+     * @param inviteCode
+     *            邀请码
+     * @return 队伍预览结果
+     */
+    TeamPreviewResult previewTeam(String inviteCode);
+
+    /**
+     * 通过邀请码加入队伍。
+     *
+     * @param inviteCode
+     *            邀请码
+     * @return 加入后的队伍结果
+     */
+    TeamResult joinTeam(String inviteCode);
+
+    /**
+     * 获取当前用户在指定考核时间下的队伍。
+     *
+     * @param assessmentTimeId
+     *            考核时间ID
+     * @return 队伍结果，未加入队伍时返回 null
+     */
+    TeamResult getMyTeam(Long assessmentTimeId);
+
+    /**
+     * 离开队伍。
+     *
+     * @param teamId
+     *            队伍ID
+     */
+    void leaveTeam(Long teamId);
+
+    /**
+     * 转让队长。
+     *
+     * @param teamId
+     *            队伍ID
+     * @param newLeaderId
+     *            新队长用户ID
+     * @return 转让后的队伍结果
+     */
+    TeamResult transferLeader(Long teamId, Long newLeaderId);
+
+    /**
+     * 解散队伍。
+     *
+     * @param teamId
+     *            队伍ID
+     */
+    void disbandTeam(Long teamId);
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImpl.java b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImpl.java
index f966ece..1695c28 100644
--- a/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImpl.java
+++ b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImpl.java
@@ -24,8 +24,10 @@ import com.bluenet.web.domain.model.vo.FileVO;
 import com.bluenet.web.domain.model.vo.UserVO;
 import com.bluenet.web.domain.model.vo.evaluation.MultipleChoiceContent;
 import com.bluenet.web.domain.model.vo.evaluation.SingleChoiceContent;
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
 import com.bluenet.web.domain.repository.AssessmentAnswerRepository;
 import com.bluenet.web.domain.repository.AssessmentSessionRepository;
+import com.bluenet.web.domain.repository.AssessmentTeamRepository;
 import com.bluenet.web.domain.service.AssessmentJudgementDomainService;
 import com.bluenet.web.domain.repository.AssessmentQuestionRepository;
 import com.bluenet.web.domain.repository.AssessmentTimeRepository;
@@ -68,6 +70,7 @@ public class AssessmentAnswerAppServiceImpl implements AssessmentAnswerAppServic
     private final AssessmentJudgementDomainService assessmentJudgementDomainService;
     private final AssessmentAnswerRepository assessmentAnswerRepository;
     private final AssessmentSessionRepository assessmentSessionRepository;
+    private final AssessmentTeamRepository assessmentTeamRepository;
     private final ObjectMapper objectMapper;
     private final UserDomainService userDomainService;
     private final CommentDomainService commentDomainService;
@@ -113,12 +116,18 @@ public class AssessmentAnswerAppServiceImpl implements AssessmentAnswerAppServic
             throw new DataConflict("已经提交过该题目的答案");
         }
 
+        Long teamId = null;
+        if (question.getQuestionType() == QuestionType.FILE_UPLOAD && Boolean.TRUE.equals(timeVO.getAllowTeam())) {
+            teamId = validateTeamLeaderForAnswer(command.userId(), timeVO.getId());
+        }
+
         AssessmentAnswer entity = AssessmentAnswer.create(
                 command.userId(),
                 command.questionId(),
                 command.content(),
                 command.language(),
-                command.fileId());
+                command.fileId(),
+                teamId);
 
         assessmentAnswerRepository.save(entity);
 
@@ -186,6 +195,10 @@ public class AssessmentAnswerAppServiceImpl implements AssessmentAnswerAppServic
                 command.fileId(),
                 command.content() != null ? command.content().length() : 0);
 
+        if (question.getQuestionType() == QuestionType.FILE_UPLOAD && Boolean.TRUE.equals(timeVO.getAllowTeam())) {
+            validateTeamLeaderForAnswer(command.userId(), timeVO.getId());
+        }
+
         if (command.fileId() != null) {
             existing.setFileId(command.fileId());
         }
@@ -232,20 +245,47 @@ public class AssessmentAnswerAppServiceImpl implements AssessmentAnswerAppServic
      */
     @Override
     public AssessmentAnswerResult getMyAnswer(Long userId, Long questionId) {
+        AssessmentQuestion question = assessmentQuestionRepository.findById(questionId)
+                .orElse(null);
+
         Optional<AssessmentAnswer> answerOpt = assessmentAnswerRepository
                 .findByUserIdAndQuestionId(userId, questionId);
+
         if (answerOpt.isEmpty()) {
+            // For FILE_UPLOAD questions in team-enabled assessments, if user is team member
+            // (not leader), return leader's answer
+            if (question != null && question.getQuestionType() == QuestionType.FILE_UPLOAD) {
+                AssessmentTime time = assessmentTimeRepository.findById(question.getAssessmentTimeId())
+                        .orElse(null);
+                if (time != null && Boolean.TRUE.equals(time.getAllowTeam())) {
+                    Optional<AssessmentTeam> teamOpt = assessmentTeamRepository
+                            .findByAssessmentTimeIdAndUserId(time.getId(), userId);
+                    if (teamOpt.isPresent()) {
+                        AssessmentTeam team = teamOpt.get();
+                        if (!team.isLeader(userId)) {
+                            Optional<AssessmentAnswer> leaderAnswerOpt = assessmentAnswerRepository
+                                    .findByUserIdAndQuestionId(team.getLeaderId(), questionId);
+                            if (leaderAnswerOpt.isPresent()) {
+                                return toAnswerResult(leaderAnswerOpt.get(), question);
+                            }
+                        }
+                    }
+                }
+            }
             return null;
         }
+
         AssessmentAnswer answer = answerOpt.get();
+        return toAnswerResult(answer, question);
+    }
+
+    private AssessmentAnswerResult toAnswerResult(AssessmentAnswer answer, AssessmentQuestion question) {
         AssessmentJudgementVO judgement = findLatestJudgement(answer);
         List<com.bluenet.web.domain.model.vo.CommentVO> comments = commentDomainService
                 .listCommentsByAnswerId(answer.getId());
         List<com.bluenet.web.domain.model.vo.CommentVO> memberComments = filterMemberCommentsOnly(comments);
         AssessmentAnswerResult result = toResult(answer, judgement, memberComments);
 
-        AssessmentQuestion question = assessmentQuestionRepository.findById(questionId)
-                .orElse(null);
         if (question != null && question.getQuestionType().isChoiceQuestion()) {
             return result.withJudgementErased();
         }
@@ -276,10 +316,27 @@ public class AssessmentAnswerAppServiceImpl implements AssessmentAnswerAppServic
                 .toList();
     }
 
+    private Long validateTeamLeaderForAnswer(Long userId, Long assessmentTimeId) {
+        Optional<AssessmentTeam> teamOpt = assessmentTeamRepository
+                .findByAssessmentTimeIdAndUserId(assessmentTimeId, userId);
+        if (teamOpt.isEmpty()) {
+            throw new BadRequest("该题目需要加入队伍后才能提交答案");
+        }
+        AssessmentTeam team = teamOpt.get();
+        if (!team.isActive()) {
+            throw new BadRequest("队伍已解散，无法提交答案");
+        }
+        if (!team.isLeader(userId)) {
+            throw new Forbidden("只有队长可以提交文件上传题的答案");
+        }
+        return team.getId();
+    }
+
     private AssessmentTime validateDirectionMatch(UserVO user, AssessmentQuestion question) {
         AssessmentTime time = assessmentTimeRepository.findById(question.getAssessmentTimeId())
                 .orElseThrow(() -> new BadRequest("考核时间不存在"));
-        if (user.getDirection() != null && !user.getDirection().equals(time.getDirection())) {
+        if (time.getDirection() != null && user.getDirection() != null
+                && !user.getDirection().equals(time.getDirection())) {
             throw new Forbidden("方向不匹配");
         }
         return time;
diff --git a/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImpl.java b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImpl.java
new file mode 100644
index 0000000..b2d32e2
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTeamAppServiceImpl.java
@@ -0,0 +1,344 @@
+package com.bluenet.web.application.service.impl;
+
+import com.bluenet.web.application.TeamPreviewResult;
+import com.bluenet.web.application.TeamResult;
+import com.bluenet.web.application.service.AssessmentTeamAppService;
+import com.bluenet.web.domain.exception.BadRequest;
+import com.bluenet.web.domain.exception.DataNotFound;
+import com.bluenet.web.domain.exception.Forbidden;
+import com.bluenet.web.domain.model.entity.AssessmentAnswer;
+import com.bluenet.web.domain.model.entity.AssessmentQuestion;
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+import com.bluenet.web.domain.model.entity.AssessmentTime;
+import com.bluenet.web.domain.model.enumerate.QuestionType;
+import com.bluenet.web.domain.model.vo.UserVO;
+import com.bluenet.web.domain.repository.AssessmentAnswerRepository;
+import com.bluenet.web.domain.repository.AssessmentQuestionRepository;
+import com.bluenet.web.domain.repository.AssessmentTeamRepository;
+import com.bluenet.web.domain.repository.AssessmentTimeRepository;
+import com.bluenet.web.domain.service.UserDomainService;
+import com.bluenet.web.infrastructure.security.util.UserCTX;
+import lombok.RequiredArgsConstructor;
+import lombok.extern.slf4j.Slf4j;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+
+import java.security.SecureRandom;
+import java.time.LocalDateTime;
+import java.util.ArrayList;
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 考核队伍应用服务实现。
+ * <p>
+ * 实现考核队伍聚合在应用层的业务逻辑编排。
+ * </p>
+ */
+@Service
+@Slf4j
+@RequiredArgsConstructor
+public class AssessmentTeamAppServiceImpl implements AssessmentTeamAppService {
+
+    private final AssessmentTeamRepository assessmentTeamRepository;
+    private final AssessmentTimeRepository assessmentTimeRepository;
+    private final AssessmentAnswerRepository assessmentAnswerRepository;
+    private final AssessmentQuestionRepository assessmentQuestionRepository;
+    private final UserDomainService userDomainService;
+
+    private static final String INVITE_CODE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
+    private static final int INVITE_CODE_LENGTH = 6;
+    private final SecureRandom secureRandom = new SecureRandom();
+
+    @Override
+    @Transactional
+    public TeamResult createTeam(Long assessmentTimeId, String name) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        AssessmentTime assessmentTime = assessmentTimeRepository.findById(assessmentTimeId)
+                .orElseThrow(() -> new DataNotFound("考核时间不存在"));
+
+        if (!Boolean.TRUE.equals(assessmentTime.getAllowTeam())) {
+            throw new BadRequest("该考核不允许组队");
+        }
+
+        validateTimeNotEnded(assessmentTime);
+
+        if (assessmentTeamRepository.existsByAssessmentTimeIdAndUserId(assessmentTimeId, currentUser.getId())) {
+            throw new BadRequest("您已加入该考核的队伍");
+        }
+
+        if (hasPersonalAnswer(assessmentTimeId, currentUser.getId())) {
+            throw new BadRequest("您已提交过个人答案，无法创建队伍");
+        }
+
+        String inviteCode = generateInviteCode();
+        while (assessmentTeamRepository.findByInviteCode(inviteCode).isPresent()) {
+            inviteCode = generateInviteCode();
+        }
+
+        AssessmentTeam team = AssessmentTeam.create(assessmentTimeId, currentUser.getId(), name, inviteCode);
+        assessmentTeamRepository.save(team);
+
+        log.info(
+                "创建队伍成功，teamId: {}, assessmentTimeId: {}, leaderId: {}",
+                team.getId(),
+                assessmentTimeId,
+                currentUser.getId());
+
+        return toTeamResult(team);
+    }
+
+    @Override
+    @Transactional(readOnly = true)
+    public TeamPreviewResult previewTeam(String inviteCode) {
+        AssessmentTeam team = assessmentTeamRepository.findByInviteCode(inviteCode)
+                .orElseThrow(() -> new DataNotFound("邀请码无效"));
+
+        AssessmentTime assessmentTime = assessmentTimeRepository.findById(team.getAssessmentTimeId())
+                .orElseThrow(() -> new DataNotFound("考核时间不存在"));
+
+        validateTimeNotEnded(assessmentTime);
+
+        List<AssessmentTeamMember> members = assessmentTeamRepository.findMembersByTeamId(team.getId());
+        List<String> memberUsernames = new ArrayList<>();
+        String leaderUsername = "";
+
+        for (AssessmentTeamMember member : members) {
+            Optional<UserVO> userOpt = userDomainService.getUser(member.getUserId());
+            if (userOpt.isPresent()) {
+                String username = userOpt.get().getUsername();
+                memberUsernames.add(username);
+                if (member.getUserId().equals(team.getLeaderId())) {
+                    leaderUsername = username;
+                }
+            }
+        }
+
+        return new TeamPreviewResult(
+                team.getId(),
+                team.getAssessmentTimeId(),
+                leaderUsername,
+                team.getName(),
+                team.getStatus(),
+                team.getCreatedAt(),
+                members.size(),
+                memberUsernames);
+    }
+
+    @Override
+    @Transactional
+    public TeamResult joinTeam(String inviteCode) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        AssessmentTeam team = assessmentTeamRepository.findByInviteCode(inviteCode)
+                .orElseThrow(() -> new DataNotFound("邀请码无效"));
+
+        if (!team.isActive()) {
+            throw new BadRequest("该队伍已解散");
+        }
+
+        AssessmentTime assessmentTime = assessmentTimeRepository.findById(team.getAssessmentTimeId())
+                .orElseThrow(() -> new DataNotFound("考核时间不存在"));
+
+        validateTimeNotEnded(assessmentTime);
+
+        if (assessmentTeamRepository
+                .existsByAssessmentTimeIdAndUserId(team.getAssessmentTimeId(), currentUser.getId())) {
+            throw new BadRequest("您已加入该考核的队伍");
+        }
+
+        if (hasPersonalAnswer(team.getAssessmentTimeId(), currentUser.getId())) {
+            throw new BadRequest("您已提交过个人答案，无法加入队伍");
+        }
+
+        assessmentTeamRepository.addMember(team.getId(), currentUser.getId());
+
+        log.info("用户加入队伍成功，teamId: {}, userId: {}", team.getId(), currentUser.getId());
+
+        AssessmentTeam updatedTeam = assessmentTeamRepository.findById(team.getId())
+                .orElseThrow(() -> new DataNotFound("队伍不存在"));
+        return toTeamResult(updatedTeam);
+    }
+
+    @Override
+    @Transactional(readOnly = true)
+    public TeamResult getMyTeam(Long assessmentTimeId) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        Optional<AssessmentTeam> teamOpt = assessmentTeamRepository
+                .findByAssessmentTimeIdAndUserId(assessmentTimeId, currentUser.getId());
+        if (teamOpt.isEmpty()) {
+            return null;
+        }
+
+        return toTeamResult(teamOpt.get());
+    }
+
+    @Override
+    @Transactional
+    public void leaveTeam(Long teamId) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        AssessmentTeam team = assessmentTeamRepository.findById(teamId)
+                .orElseThrow(() -> new DataNotFound("队伍不存在"));
+
+        if (!team.isActive()) {
+            throw new BadRequest("该队伍已解散");
+        }
+
+        if (team.isLeader(currentUser.getId())) {
+            throw new Forbidden("队长不能离开队伍，请先转让队长或解散队伍");
+        }
+
+        if (!assessmentTeamRepository.isMember(teamId, currentUser.getId())) {
+            throw new BadRequest("您不是该队伍的成员");
+        }
+
+        assessmentTeamRepository.removeMember(teamId, currentUser.getId());
+
+        log.info("用户离开队伍成功，teamId: {}, userId: {}", teamId, currentUser.getId());
+    }
+
+    @Override
+    @Transactional
+    public TeamResult transferLeader(Long teamId, Long newLeaderId) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        AssessmentTeam team = assessmentTeamRepository.findById(teamId)
+                .orElseThrow(() -> new DataNotFound("队伍不存在"));
+
+        if (!team.isActive()) {
+            throw new BadRequest("该队伍已解散");
+        }
+
+        if (!team.isLeader(currentUser.getId())) {
+            throw new Forbidden("只有队长可以转让队长");
+        }
+
+        if (!assessmentTeamRepository.isMember(teamId, newLeaderId)) {
+            throw new BadRequest("新队长必须是队伍成员");
+        }
+
+        team.updateLeader(newLeaderId);
+        assessmentTeamRepository.updateLeader(teamId, newLeaderId);
+
+        log.info("转让队长成功，teamId: {}, newLeaderId: {}", teamId, newLeaderId);
+
+        AssessmentTeam updatedTeam = assessmentTeamRepository.findById(teamId)
+                .orElseThrow(() -> new DataNotFound("队伍不存在"));
+        return toTeamResult(updatedTeam);
+    }
+
+    @Override
+    @Transactional
+    public void disbandTeam(Long teamId) {
+        UserVO currentUser = UserCTX.getCurrentUser();
+        if (currentUser == null) {
+            throw new SecurityException("未登录");
+        }
+
+        AssessmentTeam team = assessmentTeamRepository.findById(teamId)
+                .orElseThrow(() -> new DataNotFound("队伍不存在"));
+
+        if (!team.isLeader(currentUser.getId())) {
+            throw new Forbidden("只有队长可以解散队伍");
+        }
+
+        team.disband();
+        assessmentTeamRepository.update(team);
+
+        log.info("解散队伍成功，teamId: {}, leaderId: {}", teamId, currentUser.getId());
+    }
+
+    private String generateInviteCode() {
+        StringBuilder sb = new StringBuilder(INVITE_CODE_LENGTH);
+        for (int i = 0; i < INVITE_CODE_LENGTH; i++) {
+            int index = secureRandom.nextInt(INVITE_CODE_CHARS.length());
+            sb.append(INVITE_CODE_CHARS.charAt(index));
+        }
+        return sb.toString();
+    }
+
+    private void validateTimeNotEnded(AssessmentTime time) {
+        if (time.getEndTime() != null && LocalDateTime.now().isAfter(time.getEndTime())) {
+            throw new BadRequest("考核时间已结束");
+        }
+    }
+
+    private boolean hasPersonalAnswer(Long assessmentTimeId, Long userId) {
+        List<AssessmentQuestion> questions = new ArrayList<>();
+        int page = 0;
+        while (true) {
+            org.springframework.data.domain.Page<AssessmentQuestion> questionPage = assessmentQuestionRepository
+                    .findAllByTimeId(
+                            assessmentTimeId,
+                            org.springframework.data.domain.PageRequest.of(page, 100));
+            questions.addAll(questionPage.getContent());
+            if (questionPage.isLast()) {
+                break;
+            }
+            page++;
+        }
+
+        for (AssessmentQuestion question : questions) {
+            if (question.getQuestionType() == QuestionType.FILE_UPLOAD) {
+                Optional<AssessmentAnswer> answerOpt = assessmentAnswerRepository
+                        .findByUserIdAndQuestionId(userId, question.getId());
+                if (answerOpt.isPresent() && answerOpt.get().getTeamId() == null) {
+                    return true;
+                }
+            }
+        }
+        return false;
+    }
+
+    private TeamResult toTeamResult(AssessmentTeam team) {
+        List<AssessmentTeamMember> members = assessmentTeamRepository.findMembersByTeamId(team.getId());
+        List<TeamResult.TeamMemberResult> memberResults = new ArrayList<>();
+
+        for (AssessmentTeamMember member : members) {
+            Optional<UserVO> userOpt = userDomainService.getUser(member.getUserId());
+            String username = userOpt.map(UserVO::getUsername).orElse("未知用户");
+            String direction = userOpt.map(u -> u.getDirection() != null ? u.getDirection().getDescription() : null)
+                    .orElse(null);
+            Long avatarFileId = userOpt.map(UserVO::getAvatarFileId).orElse(null);
+
+            memberResults.add(
+                    new TeamResult.TeamMemberResult(
+                            member.getId(),
+                            member.getUserId(),
+                            username,
+                            direction,
+                            avatarFileId,
+                            member.getJoinedAt(),
+                            member.getUserId().equals(team.getLeaderId())));
+        }
+
+        return new TeamResult(
+                team.getId(),
+                team.getAssessmentTimeId(),
+                team.getLeaderId(),
+                team.getName(),
+                team.getInviteCode(),
+                team.getStatus(),
+                team.getCreatedAt(),
+                memberResults);
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImpl.java b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImpl.java
index 6de6254..76fd45e 100644
--- a/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImpl.java
+++ b/src/backend/src/main/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImpl.java
@@ -66,7 +66,8 @@ public class AssessmentTimeAppServiceImpl implements AssessmentTimeAppService {
                 command.startTime(),
                 command.endTime(),
                 command.timeLimit(),
-                command.timeLimitMinutes());
+                command.timeLimitMinutes(),
+                command.allowTeam());
 
         assessmentTimeRepository.save(entity);
         return toResult(entity);
@@ -122,7 +123,17 @@ public class AssessmentTimeAppServiceImpl implements AssessmentTimeAppService {
             throw new IllegalArgumentException("该方向轮次年级的考核时间已存在");
         }
 
-        existing.update(newDirection, newEpoch, newGrade, newStartTime, newEndTime, newTimeLimit, newTimeLimitMinutes);
+        Boolean newAllowTeam = command.allowTeam() != null ? command.allowTeam() : existing.getAllowTeam();
+
+        existing.update(
+                newDirection,
+                newEpoch,
+                newGrade,
+                newStartTime,
+                newEndTime,
+                newTimeLimit,
+                newTimeLimitMinutes,
+                newAllowTeam);
         assessmentTimeRepository.update(existing);
         return toResult(existing);
     }
@@ -278,6 +289,7 @@ public class AssessmentTimeAppServiceImpl implements AssessmentTimeAppService {
                 entity.getEndTime(),
                 entity.getTimeLimit(),
                 entity.getTimeLimitMinutes(),
+                entity.getAllowTeam(),
                 totalQuestions,
                 completedQuestions);
     }
diff --git a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentAnswer.java b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentAnswer.java
index a3a661b..4cb7368 100644
--- a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentAnswer.java
+++ b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentAnswer.java
@@ -17,9 +17,10 @@ public class AssessmentAnswer {
     private ProgrammingLanguage language;
     private Long fileId;
     private LocalDateTime submitTime;
+    private Long teamId;
 
     private AssessmentAnswer(Long id, Long userId, Long questionId, String content,
-            ProgrammingLanguage language, Long fileId, LocalDateTime submitTime) {
+            ProgrammingLanguage language, Long fileId, LocalDateTime submitTime, Long teamId) {
         this.id = id;
         this.userId = userId;
         this.questionId = questionId;
@@ -27,15 +28,21 @@ public class AssessmentAnswer {
         this.language = language;
         this.fileId = fileId;
         this.submitTime = submitTime;
+        this.teamId = teamId;
     }
 
     public static AssessmentAnswer create(Long userId, Long questionId, String content,
             ProgrammingLanguage language, Long fileId) {
-        return new AssessmentAnswer(null, userId, questionId, content, language, fileId, LocalDateTime.now());
+        return new AssessmentAnswer(null, userId, questionId, content, language, fileId, LocalDateTime.now(), null);
+    }
+
+    public static AssessmentAnswer create(Long userId, Long questionId, String content,
+            ProgrammingLanguage language, Long fileId, Long teamId) {
+        return new AssessmentAnswer(null, userId, questionId, content, language, fileId, LocalDateTime.now(), teamId);
     }
 
     public static AssessmentAnswer reconstruct(Long id, Long userId, Long questionId, String content,
-            ProgrammingLanguage language, Long fileId, LocalDateTime submitTime) {
-        return new AssessmentAnswer(id, userId, questionId, content, language, fileId, submitTime);
+            ProgrammingLanguage language, Long fileId, LocalDateTime submitTime, Long teamId) {
+        return new AssessmentAnswer(id, userId, questionId, content, language, fileId, submitTime, teamId);
     }
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeam.java b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeam.java
new file mode 100644
index 0000000..02c1963
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeam.java
@@ -0,0 +1,66 @@
+package com.bluenet.web.domain.model.entity;
+
+import lombok.AccessLevel;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+import java.time.LocalDateTime;
+
+/**
+ * 考核队伍聚合根
+ * <p>
+ * 承载考核队伍相关的业务规则和行为
+ * </p>
+ */
+@Data
+@NoArgsConstructor(access = AccessLevel.PRIVATE)
+public class AssessmentTeam {
+    private Long id;
+    private Long assessmentTimeId;
+    private Long leaderId;
+    private String name;
+    private String inviteCode;
+    private TeamStatus status;
+    private LocalDateTime createdAt;
+
+    private AssessmentTeam(Long id, Long assessmentTimeId, Long leaderId, String name,
+            String inviteCode, TeamStatus status, LocalDateTime createdAt) {
+        this.id = id;
+        this.assessmentTimeId = assessmentTimeId;
+        this.leaderId = leaderId;
+        this.name = name;
+        this.inviteCode = inviteCode;
+        this.status = status;
+        this.createdAt = createdAt;
+    }
+
+    public static AssessmentTeam create(Long assessmentTimeId, Long leaderId, String name, String inviteCode) {
+        return new AssessmentTeam(null, assessmentTimeId, leaderId, name, inviteCode, TeamStatus.ACTIVE,
+                LocalDateTime.now());
+    }
+
+    public static AssessmentTeam reconstruct(Long id, Long assessmentTimeId, Long leaderId, String name,
+            String inviteCode, TeamStatus status, LocalDateTime createdAt) {
+        return new AssessmentTeam(id, assessmentTimeId, leaderId, name, inviteCode, status, createdAt);
+    }
+
+    public void updateLeader(Long newLeaderId) {
+        this.leaderId = newLeaderId;
+    }
+
+    public void disband() {
+        this.status = TeamStatus.DISBANDED;
+    }
+
+    public boolean isActive() {
+        return this.status == TeamStatus.ACTIVE;
+    }
+
+    public boolean isLeader(Long userId) {
+        return this.leaderId.equals(userId);
+    }
+
+    public enum TeamStatus {
+        ACTIVE, DISBANDED
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeamMember.java b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeamMember.java
new file mode 100644
index 0000000..566e895
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTeamMember.java
@@ -0,0 +1,34 @@
+package com.bluenet.web.domain.model.entity;
+
+import lombok.AccessLevel;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+import java.time.LocalDateTime;
+
+/**
+ * 考核队伍成员值对象
+ */
+@Data
+@NoArgsConstructor(access = AccessLevel.PRIVATE)
+public class AssessmentTeamMember {
+    private Long id;
+    private Long teamId;
+    private Long userId;
+    private LocalDateTime joinedAt;
+
+    private AssessmentTeamMember(Long id, Long teamId, Long userId, LocalDateTime joinedAt) {
+        this.id = id;
+        this.teamId = teamId;
+        this.userId = userId;
+        this.joinedAt = joinedAt;
+    }
+
+    public static AssessmentTeamMember create(Long teamId, Long userId) {
+        return new AssessmentTeamMember(null, teamId, userId, LocalDateTime.now());
+    }
+
+    public static AssessmentTeamMember reconstruct(Long id, Long teamId, Long userId, LocalDateTime joinedAt) {
+        return new AssessmentTeamMember(id, teamId, userId, joinedAt);
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTime.java b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTime.java
index f328e23..3d3694e 100644
--- a/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTime.java
+++ b/src/backend/src/main/java/com/bluenet/web/domain/model/entity/AssessmentTime.java
@@ -52,10 +52,15 @@ public class AssessmentTime {
      * 考核结果发布时间，设置后考生可见评论和最终评分。
      */
     private LocalDateTime resultsPublishedAt;
+    /**
+     * 是否允许组队答题。
+     */
+    private Boolean allowTeam;
 
     private AssessmentTime(Long id, Direction direction, Integer epoch, Integer grade,
             LocalDateTime startTime, LocalDateTime endTime,
-            Boolean timeLimit, Integer timeLimitMinutes, LocalDateTime resultsPublishedAt) {
+            Boolean timeLimit, Integer timeLimitMinutes, LocalDateTime resultsPublishedAt,
+            Boolean allowTeam) {
         this.id = id;
         this.direction = direction;
         this.epoch = epoch;
@@ -65,6 +70,7 @@ public class AssessmentTime {
         this.timeLimit = timeLimit;
         this.timeLimitMinutes = timeLimitMinutes;
         this.resultsPublishedAt = resultsPublishedAt;
+        this.allowTeam = allowTeam;
     }
 
     /**
@@ -72,14 +78,15 @@ public class AssessmentTime {
      */
     public static AssessmentTime create(Direction direction, Integer epoch, Integer grade,
             LocalDateTime startTime, LocalDateTime endTime,
-            Boolean timeLimit, Integer timeLimitMinutes) {
+            Boolean timeLimit, Integer timeLimitMinutes, Boolean allowTeam) {
         if (startTime != null && endTime != null && !startTime.isBefore(endTime)) {
             throw new IllegalArgumentException("开始时间必须早于结束时间");
         }
         if (Boolean.TRUE.equals(timeLimit) && (timeLimitMinutes == null || timeLimitMinutes <= 0)) {
             throw new IllegalArgumentException("限时考核必须设置有效的限时分钟数");
         }
-        return new AssessmentTime(null, direction, epoch, grade, startTime, endTime, timeLimit, timeLimitMinutes, null);
+        return new AssessmentTime(null, direction, epoch, grade, startTime, endTime, timeLimit, timeLimitMinutes, null,
+                allowTeam);
     }
 
     /**
@@ -87,9 +94,10 @@ public class AssessmentTime {
      */
     public static AssessmentTime reconstruct(Long id, Direction direction, Integer epoch, Integer grade,
             LocalDateTime startTime, LocalDateTime endTime,
-            Boolean timeLimit, Integer timeLimitMinutes, LocalDateTime resultsPublishedAt) {
+            Boolean timeLimit, Integer timeLimitMinutes, LocalDateTime resultsPublishedAt,
+            Boolean allowTeam) {
         return new AssessmentTime(id, direction, epoch, grade, startTime, endTime, timeLimit, timeLimitMinutes,
-                resultsPublishedAt);
+                resultsPublishedAt, allowTeam);
     }
 
     /**
@@ -97,7 +105,7 @@ public class AssessmentTime {
      */
     public void update(Direction direction, Integer epoch, Integer grade,
             LocalDateTime startTime, LocalDateTime endTime,
-            Boolean timeLimit, Integer timeLimitMinutes) {
+            Boolean timeLimit, Integer timeLimitMinutes, Boolean allowTeam) {
         if (direction != null) {
             this.direction = direction;
         }
@@ -119,6 +127,9 @@ public class AssessmentTime {
         if (timeLimitMinutes != null) {
             this.timeLimitMinutes = timeLimitMinutes;
         }
+        if (allowTeam != null) {
+            this.allowTeam = allowTeam;
+        }
     }
 
     /**
diff --git a/src/backend/src/main/java/com/bluenet/web/domain/repository/AssessmentTeamRepository.java b/src/backend/src/main/java/com/bluenet/web/domain/repository/AssessmentTeamRepository.java
new file mode 100644
index 0000000..ab1287d
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/domain/repository/AssessmentTeamRepository.java
@@ -0,0 +1,40 @@
+package com.bluenet.web.domain.repository;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 考核队伍仓库接口
+ * <p>
+ * 负责考核队伍数据的持久化操作
+ * </p>
+ */
+public interface AssessmentTeamRepository {
+
+    Optional<AssessmentTeam> findById(Long id);
+
+    Optional<AssessmentTeam> findByInviteCode(String inviteCode);
+
+    Optional<AssessmentTeam> findByAssessmentTimeIdAndUserId(Long assessmentTimeId, Long userId);
+
+    boolean existsByAssessmentTimeIdAndUserId(Long assessmentTimeId, Long userId);
+
+    void save(AssessmentTeam team);
+
+    void update(AssessmentTeam team);
+
+    void deleteById(Long id);
+
+    void updateLeader(Long teamId, Long newLeaderId);
+
+    void addMember(Long teamId, Long userId);
+
+    void removeMember(Long teamId, Long userId);
+
+    List<AssessmentTeamMember> findMembersByTeamId(Long teamId);
+
+    boolean isMember(Long teamId, Long userId);
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentAnswerRepositoryConverter.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentAnswerRepositoryConverter.java
index f93ec17..b96de5d 100644
--- a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentAnswerRepositoryConverter.java
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentAnswerRepositoryConverter.java
@@ -32,6 +32,7 @@ public class AssessmentAnswerRepositoryConverter {
                 .language(entity.getLanguage())
                 .fileId(entity.getFileId())
                 .submitTime(entity.getSubmitTime())
+                .teamId(entity.getTeamId())
                 .build();
     }
 
@@ -53,6 +54,7 @@ public class AssessmentAnswerRepositoryConverter {
                 dataObject.getContent(),
                 dataObject.getLanguage(),
                 dataObject.getFileId(),
-                dataObject.getSubmitTime());
+                dataObject.getSubmitTime(),
+                dataObject.getTeamId());
     }
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTeamRepositoryConverter.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTeamRepositoryConverter.java
new file mode 100644
index 0000000..283a78c
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTeamRepositoryConverter.java
@@ -0,0 +1,80 @@
+package com.bluenet.web.infrastructure.repository.converter;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamDO;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamMemberDO;
+import org.springframework.stereotype.Component;
+
+import java.util.List;
+
+/**
+ * 考核队伍仓储转换器
+ * <p>
+ * 负责 AssessmentTeam 的 DO 与 Entity 之间的显式字段映射
+ * </p>
+ */
+@Component
+public class AssessmentTeamRepositoryConverter {
+
+    public AssessmentTeamDO toDataObject(AssessmentTeam entity) {
+        if (entity == null) {
+            return null;
+        }
+        return AssessmentTeamDO.builder()
+                .id(entity.getId())
+                .assessmentTimeId(entity.getAssessmentTimeId())
+                .leaderId(entity.getLeaderId())
+                .name(entity.getName())
+                .inviteCode(entity.getInviteCode())
+                .status(entity.getStatus() != null ? entity.getStatus().name() : null)
+                .createdAt(entity.getCreatedAt())
+                .build();
+    }
+
+    public AssessmentTeam toEntity(AssessmentTeamDO dataObject) {
+        if (dataObject == null) {
+            return null;
+        }
+        return AssessmentTeam.reconstruct(
+                dataObject.getId(),
+                dataObject.getAssessmentTimeId(),
+                dataObject.getLeaderId(),
+                dataObject.getName(),
+                dataObject.getInviteCode(),
+                dataObject.getStatus() != null ? AssessmentTeam.TeamStatus.valueOf(dataObject.getStatus()) : null,
+                dataObject.getCreatedAt());
+    }
+
+    public AssessmentTeamMemberDO toMemberDataObject(AssessmentTeamMember entity) {
+        if (entity == null) {
+            return null;
+        }
+        return AssessmentTeamMemberDO.builder()
+                .id(entity.getId())
+                .teamId(entity.getTeamId())
+                .userId(entity.getUserId())
+                .joinedAt(entity.getJoinedAt())
+                .build();
+    }
+
+    public AssessmentTeamMember toMemberEntity(AssessmentTeamMemberDO dataObject) {
+        if (dataObject == null) {
+            return null;
+        }
+        return AssessmentTeamMember.reconstruct(
+                dataObject.getId(),
+                dataObject.getTeamId(),
+                dataObject.getUserId(),
+                dataObject.getJoinedAt());
+    }
+
+    public List<AssessmentTeamMember> toMemberEntityList(List<AssessmentTeamMemberDO> dataObjects) {
+        if (dataObjects == null) {
+            return List.of();
+        }
+        return dataObjects.stream()
+                .map(this::toMemberEntity)
+                .toList();
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTimeRepositoryConverter.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTimeRepositoryConverter.java
index edabf21..97f973f 100644
--- a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTimeRepositoryConverter.java
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/converter/AssessmentTimeRepositoryConverter.java
@@ -32,6 +32,7 @@ public class AssessmentTimeRepositoryConverter {
                 .timeLimit(entity.getTimeLimit())
                 .timeLimitMinutes(entity.getTimeLimitMinutes())
                 .resultsPublishedAt(entity.getResultsPublishedAt())
+                .allowTeam(entity.getAllowTeam())
                 .build();
     }
 
@@ -51,7 +52,8 @@ public class AssessmentTimeRepositoryConverter {
                 dataObject.getEndTime(),
                 dataObject.getTimeLimit(),
                 dataObject.getTimeLimitMinutes(),
-                dataObject.getResultsPublishedAt());
+                dataObject.getResultsPublishedAt(),
+                dataObject.getAllowTeam());
     }
 
     /**
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentAnswerDO.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentAnswerDO.java
index ce1d65b..a9f7b0f 100644
--- a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentAnswerDO.java
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentAnswerDO.java
@@ -51,4 +51,9 @@ public class AssessmentAnswerDO {
      * 答案提交时间。
      */
     private LocalDateTime submitTime;
+
+    /**
+     * 队伍ID，组队题时关联到队伍。
+     */
+    private Long teamId;
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamDO.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamDO.java
new file mode 100644
index 0000000..c2a12f6
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamDO.java
@@ -0,0 +1,36 @@
+package com.bluenet.web.infrastructure.repository.dataobject;
+
+import com.baomidou.mybatisplus.annotation.IdType;
+import com.baomidou.mybatisplus.annotation.TableId;
+import com.baomidou.mybatisplus.annotation.TableName;
+import java.time.LocalDateTime;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * Mapper 专用数据对象，只承载数据库表字段，避免持久层依赖领域实体行为。
+ */
+@Data
+@Builder
+@NoArgsConstructor
+@AllArgsConstructor
+@TableName("tb_assessment_team")
+public class AssessmentTeamDO {
+
+    @TableId(type = IdType.AUTO)
+    private Long id;
+
+    private Long assessmentTimeId;
+
+    private Long leaderId;
+
+    private String name;
+
+    private String inviteCode;
+
+    private String status;
+
+    private LocalDateTime createdAt;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamMemberDO.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamMemberDO.java
new file mode 100644
index 0000000..ab20be3
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTeamMemberDO.java
@@ -0,0 +1,30 @@
+package com.bluenet.web.infrastructure.repository.dataobject;
+
+import com.baomidou.mybatisplus.annotation.IdType;
+import com.baomidou.mybatisplus.annotation.TableId;
+import com.baomidou.mybatisplus.annotation.TableName;
+import java.time.LocalDateTime;
+import lombok.AllArgsConstructor;
+import lombok.Builder;
+import lombok.Data;
+import lombok.NoArgsConstructor;
+
+/**
+ * Mapper 专用数据对象，只承载数据库表字段，避免持久层依赖领域实体行为。
+ */
+@Data
+@Builder
+@NoArgsConstructor
+@AllArgsConstructor
+@TableName("tb_assessment_team_member")
+public class AssessmentTeamMemberDO {
+
+    @TableId(type = IdType.AUTO)
+    private Long id;
+
+    private Long teamId;
+
+    private Long userId;
+
+    private LocalDateTime joinedAt;
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTimeDO.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTimeDO.java
index 888f482..578b40e 100644
--- a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTimeDO.java
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/dataobject/AssessmentTimeDO.java
@@ -61,4 +61,9 @@ public class AssessmentTimeDO {
      * 考核结果发布时间，设置后考生可见评论和最终评分。
      */
     private LocalDateTime resultsPublishedAt;
+
+    /**
+     * 是否允许组队答题。
+     */
+    private Boolean allowTeam;
 }
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImpl.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImpl.java
new file mode 100644
index 0000000..b7df316
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTeamRepositoryImpl.java
@@ -0,0 +1,107 @@
+package com.bluenet.web.infrastructure.repository.impl;
+
+import com.bluenet.web.domain.model.entity.AssessmentTeam;
+import com.bluenet.web.domain.model.entity.AssessmentTeamMember;
+import com.bluenet.web.domain.repository.AssessmentTeamRepository;
+import com.bluenet.web.infrastructure.repository.converter.AssessmentTeamRepositoryConverter;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamDO;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamMemberDO;
+import com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMapper;
+import com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMemberMapper;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Repository;
+
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 考核队伍仓库实现类
+ */
+@Repository
+@RequiredArgsConstructor
+public class AssessmentTeamRepositoryImpl implements AssessmentTeamRepository {
+
+    private final AssessmentTeamMapper assessmentTeamMapper;
+    private final AssessmentTeamMemberMapper assessmentTeamMemberMapper;
+    private final AssessmentTeamRepositoryConverter converter;
+
+    @Override
+    public Optional<AssessmentTeam> findById(Long id) {
+        AssessmentTeamDO dataObject = assessmentTeamMapper.selectById(id);
+        return Optional.ofNullable(converter.toEntity(dataObject));
+    }
+
+    @Override
+    public Optional<AssessmentTeam> findByInviteCode(String inviteCode) {
+        AssessmentTeamDO dataObject = assessmentTeamMapper.selectByInviteCode(inviteCode);
+        return Optional.ofNullable(converter.toEntity(dataObject));
+    }
+
+    @Override
+    public Optional<AssessmentTeam> findByAssessmentTimeIdAndUserId(Long assessmentTimeId, Long userId) {
+        AssessmentTeamDO dataObject = assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(assessmentTimeId, userId);
+        return Optional.ofNullable(converter.toEntity(dataObject));
+    }
+
+    @Override
+    public boolean existsByAssessmentTimeIdAndUserId(Long assessmentTimeId, Long userId) {
+        return assessmentTeamMapper.selectByAssessmentTimeIdAndUserId(assessmentTimeId, userId) != null;
+    }
+
+    @Override
+    public void save(AssessmentTeam team) {
+        AssessmentTeamDO dataObject = converter.toDataObject(team);
+        assessmentTeamMapper.insert(dataObject);
+        team.setId(dataObject.getId());
+
+        AssessmentTeamMemberDO leaderMember = AssessmentTeamMemberDO.builder()
+                .teamId(dataObject.getId())
+                .userId(team.getLeaderId())
+                .build();
+        assessmentTeamMemberMapper.insert(leaderMember);
+    }
+
+    @Override
+    public void update(AssessmentTeam team) {
+        AssessmentTeamDO dataObject = converter.toDataObject(team);
+        assessmentTeamMapper.updateById(dataObject);
+    }
+
+    @Override
+    public void deleteById(Long id) {
+        assessmentTeamMemberMapper.delete(
+                new com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper<AssessmentTeamMemberDO>()
+                        .eq(AssessmentTeamMemberDO::getTeamId, id));
+        assessmentTeamMapper.deleteById(id);
+    }
+
+    @Override
+    public void updateLeader(Long teamId, Long newLeaderId) {
+        assessmentTeamMapper.updateLeader(teamId, newLeaderId);
+    }
+
+    @Override
+    public void addMember(Long teamId, Long userId) {
+        AssessmentTeamMemberDO member = AssessmentTeamMemberDO.builder()
+                .teamId(teamId)
+                .userId(userId)
+                .build();
+        assessmentTeamMemberMapper.insert(member);
+    }
+
+    @Override
+    public void removeMember(Long teamId, Long userId) {
+        assessmentTeamMemberMapper.deleteByTeamIdAndUserId(teamId, userId);
+    }
+
+    @Override
+    public List<AssessmentTeamMember> findMembersByTeamId(Long teamId) {
+        List<AssessmentTeamMemberDO> dataObjects = assessmentTeamMemberMapper.selectByTeamId(teamId);
+        return converter.toMemberEntityList(dataObjects);
+    }
+
+    @Override
+    public boolean isMember(Long teamId, Long userId) {
+        return assessmentTeamMemberMapper.existsByTeamIdAndUserId(teamId, userId);
+    }
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMapper.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMapper.java
new file mode 100644
index 0000000..3e3e252
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMapper.java
@@ -0,0 +1,23 @@
+package com.bluenet.web.infrastructure.repository.mapper;
+
+import com.baomidou.mybatisplus.core.mapper.BaseMapper;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamDO;
+import org.apache.ibatis.annotations.Mapper;
+import org.apache.ibatis.annotations.Param;
+import org.apache.ibatis.annotations.Update;
+
+import java.util.List;
+
+@Mapper
+public interface AssessmentTeamMapper extends BaseMapper<AssessmentTeamDO> {
+
+    AssessmentTeamDO selectByInviteCode(@Param("inviteCode") String inviteCode);
+
+    AssessmentTeamDO selectByAssessmentTimeIdAndUserId(@Param("assessmentTimeId") Long assessmentTimeId,
+            @Param("userId") Long userId);
+
+    @Update("UPDATE tb_assessment_team SET leader_id = #{newLeaderId} WHERE id = #{teamId}")
+    int updateLeader(@Param("teamId") Long teamId, @Param("newLeaderId") Long newLeaderId);
+
+    List<Long> selectMemberUserIdsByTeamId(@Param("teamId") Long teamId);
+}
diff --git a/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMemberMapper.java b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMemberMapper.java
new file mode 100644
index 0000000..cb6cc5f
--- /dev/null
+++ b/src/backend/src/main/java/com/bluenet/web/infrastructure/repository/mapper/AssessmentTeamMemberMapper.java
@@ -0,0 +1,18 @@
+package com.bluenet.web.infrastructure.repository.mapper;
+
+import com.baomidou.mybatisplus.core.mapper.BaseMapper;
+import com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamMemberDO;
+import org.apache.ibatis.annotations.Mapper;
+import org.apache.ibatis.annotations.Param;
+
+import java.util.List;
+
+@Mapper
+public interface AssessmentTeamMemberMapper extends BaseMapper<AssessmentTeamMemberDO> {
+
+    List<AssessmentTeamMemberDO> selectByTeamId(@Param("teamId") Long teamId);
+
+    int deleteByTeamIdAndUserId(@Param("teamId") Long teamId, @Param("userId") Long userId);
+
+    boolean existsByTeamIdAndUserId(@Param("teamId") Long teamId, @Param("userId") Long userId);
+}
diff --git a/src/backend/src/main/resources/db/migration/V13__add_team_support_to_assessment.sql b/src/backend/src/main/resources/db/migration/V13__add_team_support_to_assessment.sql
new file mode 100644
index 0000000..628a287
--- /dev/null
+++ b/src/backend/src/main/resources/db/migration/V13__add_team_support_to_assessment.sql
@@ -0,0 +1,15 @@
+-- 为考核系统添加组队支持
+-- 1. 考核时间表增加 allow_team 字段，标识该考核是否允许组队
+-- 2. 答案表增加 team_id 字段，用于关联队伍答案
+
+ALTER TABLE tb_assessment_time
+    ADD COLUMN allow_team BOOLEAN NOT NULL DEFAULT FALSE;
+
+COMMENT ON COLUMN tb_assessment_time.allow_team IS '是否允许组队，默认 false';
+
+ALTER TABLE tb_assessment_answer
+    ADD COLUMN team_id BIGINT;
+
+COMMENT ON COLUMN tb_assessment_answer.team_id IS '队伍ID，组队题时关联到队伍';
+
+CREATE INDEX idx_asm_answer_team_id ON tb_assessment_answer(team_id);
diff --git a/src/backend/src/main/resources/db/migration/V14__create_assessment_team_tables.sql b/src/backend/src/main/resources/db/migration/V14__create_assessment_team_tables.sql
new file mode 100644
index 0000000..e0785ef
--- /dev/null
+++ b/src/backend/src/main/resources/db/migration/V14__create_assessment_team_tables.sql
@@ -0,0 +1,41 @@
+-- 创建考核队伍表和队伍成员表
+
+CREATE TABLE tb_assessment_team (
+    id SERIAL PRIMARY KEY,
+    assessment_time_id BIGINT NOT NULL,
+    leader_id BIGINT NOT NULL,
+    name VARCHAR(100) NOT NULL,
+    invite_code VARCHAR(10) NOT NULL UNIQUE,
+    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
+    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
+);
+
+COMMENT ON TABLE tb_assessment_team IS '考核队伍表';
+COMMENT ON COLUMN tb_assessment_team.id IS '队伍ID';
+COMMENT ON COLUMN tb_assessment_team.assessment_time_id IS '所属考核时间ID';
+COMMENT ON COLUMN tb_assessment_team.leader_id IS '队长用户ID';
+COMMENT ON COLUMN tb_assessment_team.name IS '队伍名称';
+COMMENT ON COLUMN tb_assessment_team.invite_code IS '邀请码，唯一';
+COMMENT ON COLUMN tb_assessment_team.status IS '队伍状态：ACTIVE/DISBANDED';
+COMMENT ON COLUMN tb_assessment_team.created_at IS '创建时间';
+
+CREATE INDEX idx_asm_team_time_id ON tb_assessment_team(assessment_time_id);
+CREATE INDEX idx_asm_team_leader_id ON tb_assessment_team(leader_id);
+CREATE INDEX idx_asm_team_invite_code ON tb_assessment_team(invite_code);
+
+CREATE TABLE tb_assessment_team_member (
+    id SERIAL PRIMARY KEY,
+    team_id BIGINT NOT NULL,
+    user_id BIGINT NOT NULL,
+    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
+    UNIQUE(team_id, user_id)
+);
+
+COMMENT ON TABLE tb_assessment_team_member IS '考核队伍成员表';
+COMMENT ON COLUMN tb_assessment_team_member.id IS '成员记录ID';
+COMMENT ON COLUMN tb_assessment_team_member.team_id IS '所属队伍ID';
+COMMENT ON COLUMN tb_assessment_team_member.user_id IS '成员用户ID';
+COMMENT ON COLUMN tb_assessment_team_member.joined_at IS '加入时间';
+
+CREATE INDEX idx_asm_team_member_team_id ON tb_assessment_team_member(team_id);
+CREATE INDEX idx_asm_team_member_user_id ON tb_assessment_team_member(user_id);
diff --git a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentAnswerMapper.xml b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentAnswerMapper.xml
index 93de8cc..9b5e7d3 100644
--- a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentAnswerMapper.xml
+++ b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentAnswerMapper.xml
@@ -9,6 +9,7 @@
         <result column="language" property="language"/>
         <result column="file_id" property="fileId"/>
         <result column="submit_time" property="submitTime"/>
+        <result column="team_id" property="teamId"/>
     </resultMap>
 
     <select id="countByUserIdAndAssessmentTimeId" resultType="int">
diff --git a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMapper.xml b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMapper.xml
new file mode 100644
index 0000000..b1401c8
--- /dev/null
+++ b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMapper.xml
@@ -0,0 +1,29 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
+<mapper namespace="com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMapper">
+    <resultMap id="BaseResultMap" type="com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamDO">
+        <id column="id" property="id"/>
+        <result column="assessment_time_id" property="assessmentTimeId"/>
+        <result column="leader_id" property="leaderId"/>
+        <result column="name" property="name"/>
+        <result column="invite_code" property="inviteCode"/>
+        <result column="status" property="status"/>
+        <result column="created_at" property="createdAt"/>
+    </resultMap>
+
+    <select id="selectByInviteCode" resultMap="BaseResultMap">
+        SELECT * FROM tb_assessment_team WHERE invite_code = #{inviteCode}
+    </select>
+
+    <select id="selectByAssessmentTimeIdAndUserId" resultMap="BaseResultMap">
+        SELECT t.* FROM tb_assessment_team t
+        INNER JOIN tb_assessment_team_member m ON m.team_id = t.id
+        WHERE t.assessment_time_id = #{assessmentTimeId}
+          AND m.user_id = #{userId}
+          AND t.status = 'ACTIVE'
+    </select>
+
+    <select id="selectMemberUserIdsByTeamId" resultType="java.lang.Long">
+        SELECT user_id FROM tb_assessment_team_member WHERE team_id = #{teamId}
+    </select>
+</mapper>
diff --git a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMemberMapper.xml b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMemberMapper.xml
new file mode 100644
index 0000000..02a72f1
--- /dev/null
+++ b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTeamMemberMapper.xml
@@ -0,0 +1,22 @@
+<?xml version="1.0" encoding="UTF-8"?>
+<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
+<mapper namespace="com.bluenet.web.infrastructure.repository.mapper.AssessmentTeamMemberMapper">
+    <resultMap id="BaseResultMap" type="com.bluenet.web.infrastructure.repository.dataobject.AssessmentTeamMemberDO">
+        <id column="id" property="id"/>
+        <result column="team_id" property="teamId"/>
+        <result column="user_id" property="userId"/>
+        <result column="joined_at" property="joinedAt"/>
+    </resultMap>
+
+    <select id="selectByTeamId" resultMap="BaseResultMap">
+        SELECT * FROM tb_assessment_team_member WHERE team_id = #{teamId}
+    </select>
+
+    <delete id="deleteByTeamIdAndUserId">
+        DELETE FROM tb_assessment_team_member WHERE team_id = #{teamId} AND user_id = #{userId}
+    </delete>
+
+    <select id="existsByTeamIdAndUserId" resultType="boolean">
+        SELECT EXISTS(SELECT 1 FROM tb_assessment_team_member WHERE team_id = #{teamId} AND user_id = #{userId})
+    </select>
+</mapper>
diff --git a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTimeMapper.xml b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTimeMapper.xml
index c3ded8a..cb8cc5d 100644
--- a/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTimeMapper.xml
+++ b/src/backend/src/main/resources/infrastructure/repository/mapper/AssessmentTimeMapper.xml
@@ -63,11 +63,12 @@
         (
             <choose>
                 <when test="direction != null and enrollmentYear != null">
-                    t.direction = #{direction}
-                    AND t.grade = #{enrollmentYear}
+                    (t.direction = #{direction} AND t.grade = #{enrollmentYear})
+                    OR (t.direction IS NULL AND t.grade = #{enrollmentYear})
                 </when>
                 <when test="direction != null">
                     t.direction = #{direction}
+                    OR t.direction IS NULL
                 </when>
                 <when test="enrollmentYear != null">
                     t.grade = #{enrollmentYear}
diff --git a/src/backend/src/test/java/com/bluenet/web/api/controller/v1/admin/AdminCommentControllerIntegrationTest.java b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/admin/AdminCommentControllerIntegrationTest.java
index 657807d..9fe2a59 100644
--- a/src/backend/src/test/java/com/bluenet/web/api/controller/v1/admin/AdminCommentControllerIntegrationTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/admin/AdminCommentControllerIntegrationTest.java
@@ -161,7 +161,8 @@ class AdminCommentControllerIntegrationTest extends BaseIntegrationTest {
                 LocalDateTime.now().minusDays(1),
                 LocalDateTime.now().plusDays(7),
                 false,
-                null);
+                null,
+                false);
         RepositoryTestObjects.insert(assessmentTimeMapper, assessmentTime, AssessmentTimeDO.class);
 
         // 创建文件上传题
diff --git a/src/backend/src/test/java/com/bluenet/web/api/controller/v1/file/FileUploadDownloadIntegrationTest.java b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/file/FileUploadDownloadIntegrationTest.java
index 3669b99..374e522 100644
--- a/src/backend/src/test/java/com/bluenet/web/api/controller/v1/file/FileUploadDownloadIntegrationTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/api/controller/v1/file/FileUploadDownloadIntegrationTest.java
@@ -200,13 +200,13 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, user, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(100L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(100L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(100L, 100L, 1, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentQuestionMapper, question, AssessmentQuestionDO.class);
 
-        AssessmentAnswer answer = AssessmentAnswer.reconstruct(100L, 100L, 100L, null, null, null, null);
+        AssessmentAnswer answer = AssessmentAnswer.reconstruct(100L, 100L, 100L, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentAnswerMapper, answer, AssessmentAnswerDO.class);
 
         FileVO workFileVO = createFileInMinio("work.zip", FileType.WORK);
@@ -247,13 +247,13 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, submitter, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(101L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(101L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(101L, 101L, 1, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentQuestionMapper, question, AssessmentQuestionDO.class);
 
-        AssessmentAnswer answer = AssessmentAnswer.reconstruct(101L, 102L, 101L, null, null, null, null);
+        AssessmentAnswer answer = AssessmentAnswer.reconstruct(101L, 102L, 101L, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentAnswerMapper, answer, AssessmentAnswerDO.class);
 
         FileVO workFileVO = createFileInMinio("work.zip", FileType.WORK);
@@ -292,13 +292,13 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, submitter, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(102L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(102L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(102L, 102L, 1, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentQuestionMapper, question, AssessmentQuestionDO.class);
 
-        AssessmentAnswer answer = AssessmentAnswer.reconstruct(102L, 104L, 102L, null, null, null, null);
+        AssessmentAnswer answer = AssessmentAnswer.reconstruct(102L, 104L, 102L, null, null, null, null, null);
         RepositoryTestObjects.insert(assessmentAnswerMapper, answer, AssessmentAnswerDO.class);
 
         FileVO workFileVO = createFileInMinio("work.zip", FileType.WORK);
@@ -339,7 +339,7 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, user, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(103L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(103L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(103L, 103L, 1, null, null, null, null, null);
@@ -383,7 +383,7 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, user, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(104L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(104L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(104L, 104L, 1, null, null, null, null, null);
@@ -455,7 +455,7 @@ class FileUploadDownloadIntegrationTest extends BaseIntegrationTest {
         RepositoryTestObjects.insert(userMapper, user, UserDO.class);
 
         AssessmentTime time = AssessmentTime
-                .reconstruct(105L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null);
+                .reconstruct(105L, Direction.COMPUTER_VISION, null, null, null, null, false, null, null, null);
         RepositoryTestObjects.insert(assessmentTimeMapper, time, AssessmentTimeDO.class);
 
         AssessmentQuestion question = AssessmentQuestion.reconstruct(105L, 105L, 1, null, null, null, null, null);
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
index e768c0c..10151ea 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AlgorithmJudgeAppServiceImplTest.java
@@ -276,6 +276,7 @@ class AlgorithmJudgeAppServiceImplTest {
                                         null,
                                         false,
                                         null,
+                                        null,
                                         null)));
     }
 
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImplTest.java
index 5adc09b..d2efc1e 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentAnswerAppServiceImplTest.java
@@ -100,7 +100,8 @@ class AssessmentAnswerAppServiceImplTest {
                 "test answer content",
                 null,
                 TEST_FILE_ID,
-                TEST_SUBMIT_TIME);
+                TEST_SUBMIT_TIME,
+                null);
     }
 
     private AssessmentQuestion createTestQuestion() {
@@ -165,7 +166,17 @@ class AssessmentAnswerAppServiceImplTest {
 
     private AssessmentTime createTestTime() {
         return AssessmentTime
-                .reconstruct(TEST_ASSESSMENT_TIME_ID, Direction.COMPUTER_VISION, 1, 2024, null, null, true, 90, null);
+                .reconstruct(
+                        TEST_ASSESSMENT_TIME_ID,
+                        Direction.COMPUTER_VISION,
+                        1,
+                        2024,
+                        null,
+                        null,
+                        true,
+                        90,
+                        null,
+                        false);
     }
 
     private AssessmentTime createNonTimedTime() {
@@ -179,7 +190,8 @@ class AssessmentAnswerAppServiceImplTest {
                         null,
                         false,
                         null,
-                        null);
+                        null,
+                        false);
     }
 
     private void stubDirectionAndFileValidation() {
@@ -390,7 +402,8 @@ class AssessmentAnswerAppServiceImplTest {
                     "[\"B\",\"A\"]",
                     null,
                     TEST_FILE_ID,
-                    TEST_SUBMIT_TIME);
+                    TEST_SUBMIT_TIME,
+                    null);
             when(assessmentQuestionRepository.findById(TEST_QUESTION_ID)).thenReturn(Optional.of(question));
             when(assessmentTimeRepository.findById(TEST_ASSESSMENT_TIME_ID)).thenReturn(Optional.of(createTestTime()));
             when(assessmentSessionRepository.findByUserIdAndAssessmentTimeId(TEST_USER_ID, TEST_ASSESSMENT_TIME_ID))
@@ -420,7 +433,8 @@ class AssessmentAnswerAppServiceImplTest {
                     "A,B",
                     null,
                     TEST_FILE_ID,
-                    TEST_SUBMIT_TIME);
+                    TEST_SUBMIT_TIME,
+                    null);
             when(assessmentQuestionRepository.findById(TEST_QUESTION_ID)).thenReturn(Optional.of(question));
             when(assessmentTimeRepository.findById(TEST_ASSESSMENT_TIME_ID)).thenReturn(Optional.of(createTestTime()));
             when(assessmentSessionRepository.findByUserIdAndAssessmentTimeId(TEST_USER_ID, TEST_ASSESSMENT_TIME_ID))
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentJudgementAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentJudgementAppServiceImplTest.java
index 1fce822..e08513a 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentJudgementAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentJudgementAppServiceImplTest.java
@@ -689,7 +689,7 @@ class AssessmentJudgementAppServiceImplTest {
     }
 
     private AssessmentAnswer createAnswerEntity() {
-        return AssessmentAnswer.reconstruct(ANSWER_ID, CANDIDATE_ID, QUESTION_ID, null, null, null, null);
+        return AssessmentAnswer.reconstruct(ANSWER_ID, CANDIDATE_ID, QUESTION_ID, null, null, null, null, null);
     }
 
     private AssessmentQuestion createQuestion(QuestionType questionType) {
@@ -754,7 +754,8 @@ class AssessmentJudgementAppServiceImplTest {
                 null,
                 false,
                 null,
-                null);
+                null,
+                false);
     }
 
     private AssessmentQuestionSubmissionVO createSubmissionVO(boolean judged) {
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentQuestionAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentQuestionAppServiceImplTest.java
index 35b3daa..fdc1de7 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentQuestionAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentQuestionAppServiceImplTest.java
@@ -81,7 +81,8 @@ class AssessmentQuestionAppServiceImplTest {
                 null,
                 true,
                 120,
-                null);
+                null,
+                false);
     }
 
     @Test
diff --git a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImplTest.java b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImplTest.java
index 2a8b57f..b868b28 100644
--- a/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/application/service/impl/AssessmentTimeAppServiceImplTest.java
@@ -66,7 +66,8 @@ class AssessmentTimeAppServiceImplTest {
                 futureEnd,
                 true,
                 120,
-                null);
+                null,
+                false);
     }
 
     // ==================== createAssessmentTime 测试 ====================
@@ -79,7 +80,7 @@ class AssessmentTimeAppServiceImplTest {
         @DisplayName("正常创建：应返回Result")
         void create_validCommand_shouldReturnResult() {
             AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, true, 120);
+                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, true, 120, false);
 
             when(assessmentTimeRepository.existsByDirectionAndEpochAndGrade(any(), any(), any())).thenReturn(false);
 
@@ -94,7 +95,7 @@ class AssessmentTimeAppServiceImplTest {
         @DisplayName("重复组合：应抛出IllegalArgumentException")
         void create_duplicateCombination_shouldThrow() {
             AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, false, null);
+                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, false, null, false);
 
             when(assessmentTimeRepository.existsByDirectionAndEpochAndGrade(any(), any(), any())).thenReturn(true);
 
@@ -108,7 +109,7 @@ class AssessmentTimeAppServiceImplTest {
         @DisplayName("开始时间不早于结束时间：应抛出IllegalArgumentException")
         void create_startTimeNotBeforeEndTime_shouldThrow() {
             AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                    Direction.COMPUTER_VISION, 1, 2024, futureEnd, futureStart, false, null);
+                    Direction.COMPUTER_VISION, 1, 2024, futureEnd, futureStart, false, null, false);
 
             IllegalArgumentException ex = assertThrows(
                     IllegalArgumentException.class,
@@ -120,7 +121,7 @@ class AssessmentTimeAppServiceImplTest {
         @DisplayName("限时考核未设置限时分钟数：应抛出IllegalArgumentException")
         void create_timeLimitWithoutMinutes_shouldThrow() {
             AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, true, null);
+                    Direction.COMPUTER_VISION, 1, 2024, futureStart, futureEnd, true, null, false);
 
             IllegalArgumentException ex = assertThrows(
                     IllegalArgumentException.class,
@@ -140,7 +141,7 @@ class AssessmentTimeAppServiceImplTest {
         void update_validCommand_shouldReturnResult() {
             AssessmentTime existing = createTestEntity();
             AssessmentTimeCommands.UpdateAssessmentTimeCommand command = new AssessmentTimeCommands.UpdateAssessmentTimeCommand(
-                    TEST_ID, null, null, null, futureStart, futureEnd, true, 90);
+                    TEST_ID, null, null, null, futureStart, futureEnd, true, 90, false);
 
             when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.of(existing));
 
@@ -154,7 +155,7 @@ class AssessmentTimeAppServiceImplTest {
         @DisplayName("更新不存在记录：应抛出DataNotFound")
         void update_notFound_shouldThrow() {
             AssessmentTimeCommands.UpdateAssessmentTimeCommand command = new AssessmentTimeCommands.UpdateAssessmentTimeCommand(
-                    TEST_ID, null, null, null, null, null, null, null);
+                    TEST_ID, null, null, null, null, null, null, null, null);
 
             when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.empty());
 
@@ -175,10 +176,11 @@ class AssessmentTimeAppServiceImplTest {
                     futureEnd,
                     false,
                     null,
-                    null);
+                    null,
+                    false);
 
             AssessmentTimeCommands.UpdateAssessmentTimeCommand command = new AssessmentTimeCommands.UpdateAssessmentTimeCommand(
-                    TEST_ID, null, null, null, LocalDateTime.of(2025, 6, 1, 9, 0), null, null, null);
+                    TEST_ID, null, null, null, LocalDateTime.of(2025, 6, 1, 9, 0), null, null, null, null);
 
             when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.of(existing));
 
@@ -248,7 +250,7 @@ class AssessmentTimeAppServiceImplTest {
                 mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(userVO);
 
                 AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                        Direction.COMPUTER_VISION, 1, 2025, futureStart, futureEnd, false, null);
+                        Direction.COMPUTER_VISION, 1, 2025, futureStart, futureEnd, false, null, false);
 
                 when(assessmentTimeRepository.existsByDirectionAndEpochAndGrade(any(), any(), any())).thenReturn(false);
 
@@ -271,7 +273,7 @@ class AssessmentTimeAppServiceImplTest {
                 mockedUserCTX.when(UserCTX::getCurrentUser).thenReturn(userVO);
 
                 AssessmentTimeCommands.CreateAssessmentTimeCommand command = new AssessmentTimeCommands.CreateAssessmentTimeCommand(
-                        Direction.STRUCTURAL_DESIGN, 1, 2025, futureStart, futureEnd, false, null);
+                        Direction.STRUCTURAL_DESIGN, 1, 2025, futureStart, futureEnd, false, null, false);
 
                 Forbidden ex = assertThrows(
                         Forbidden.class,
@@ -295,7 +297,7 @@ class AssessmentTimeAppServiceImplTest {
                 when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.of(existing));
 
                 AssessmentTimeCommands.UpdateAssessmentTimeCommand command = new AssessmentTimeCommands.UpdateAssessmentTimeCommand(
-                        TEST_ID, null, null, null, null, null, null, 90);
+                        TEST_ID, null, null, null, null, null, null, 90, false);
 
                 AssessmentTimeResult result = assessmentTimeAppService.updateAssessmentTime(command);
 
@@ -323,11 +325,12 @@ class AssessmentTimeAppServiceImplTest {
                         futureEnd,
                         false,
                         null,
-                        null);
+                        null,
+                        false);
                 when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.of(existing));
 
                 AssessmentTimeCommands.UpdateAssessmentTimeCommand command = new AssessmentTimeCommands.UpdateAssessmentTimeCommand(
-                        TEST_ID, null, null, null, null, null, null, 90);
+                        TEST_ID, null, null, null, null, null, null, 90, false);
 
                 Forbidden ex = assertThrows(
                         Forbidden.class,
@@ -377,7 +380,8 @@ class AssessmentTimeAppServiceImplTest {
                         futureEnd,
                         false,
                         null,
-                        null);
+                        null,
+                        false);
                 when(assessmentTimeRepository.findById(TEST_ID)).thenReturn(Optional.of(existing));
 
                 Forbidden ex = assertThrows(
diff --git a/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTimeRepositoryImplTest.java b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTimeRepositoryImplTest.java
index 686771d..0b7b69b 100644
--- a/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTimeRepositoryImplTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/impl/AssessmentTimeRepositoryImplTest.java
@@ -45,7 +45,7 @@ class AssessmentTimeRepositoryImplTest {
     private static final LocalDateTime END_TIME = LocalDateTime.of(2099, 1, 1, 11, 0);
 
     private AssessmentTime createTestEntity(Long id, Direction direction, int epoch, int grade) {
-        return AssessmentTime.reconstruct(id, direction, epoch, grade, START_TIME, END_TIME, false, null, null);
+        return AssessmentTime.reconstruct(id, direction, epoch, grade, START_TIME, END_TIME, false, null, null, false);
     }
 
     private AssessmentTimeDO toDataObject(AssessmentTime entity) {
@@ -77,7 +77,8 @@ class AssessmentTimeRepositoryImplTest {
                     END_TIME,
                     false,
                     null,
-                    null);
+                    null,
+                    false);
 
             assessmentTimeRepository.update(entity);
 
diff --git a/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/mapper/EntityCrudTest.java b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/mapper/EntityCrudTest.java
index 9b767de..3ae978f 100644
--- a/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/mapper/EntityCrudTest.java
+++ b/src/backend/src/test/java/com/bluenet/web/infrastructure/repository/mapper/EntityCrudTest.java
@@ -99,7 +99,8 @@ class EntityCrudTest extends BaseIntegrationTest {
                 LocalDateTime.now(),
                 LocalDateTime.now().plusDays(7),
                 true,
-                120);
+                120,
+                false);
         RepositoryTestObjects.insert(assessmentTimeMapper, evalTime, AssessmentTimeDO.class);
 
         // 创建题目 - 单选题
@@ -148,7 +149,8 @@ class EntityCrudTest extends BaseIntegrationTest {
                 LocalDateTime.now(),
                 LocalDateTime.now().plusDays(7),
                 false,
-                null);
+                null,
+                false);
         RepositoryTestObjects.insert(assessmentTimeMapper, evalTime, AssessmentTimeDO.class);
 
         AlgorithmContent content = new AlgorithmContent();
diff --git a/src/frontend/src/apis/schema/assessment.dto.ts b/src/frontend/src/apis/schema/assessment.dto.ts
index 7878f84..23b39b6 100644
--- a/src/frontend/src/apis/schema/assessment.dto.ts
+++ b/src/frontend/src/apis/schema/assessment.dto.ts
@@ -47,6 +47,8 @@ export interface CreateAssessmentTimeRequestDTO {
   timeLimit: boolean
   /** 限时分钟数（timeLimit为true时必填） */
   timeLimitMinutes?: number | null
+  /** 是否允许组队 */
+  allowTeam: boolean
 }
 
 /** 更新考核时间请求 - 对应后端 UpdateAssessmentTimeRequestDTO */
@@ -65,6 +67,8 @@ export interface UpdateAssessmentTimeRequestDTO {
   timeLimit?: boolean
   /** 限时分钟数 */
   timeLimitMinutes?: number | null
+  /** 是否允许组队 */
+  allowTeam?: boolean
 }
 
 /** 考核时间信息 - 对应后端 AssessmentTimeDTO */
@@ -85,6 +89,8 @@ export interface AssessmentTimeDTO {
   timeLimit: boolean
   /** 限时分钟数 */
   timeLimitMinutes: number | null
+  /** 是否允许组队 */
+  allowTeam: boolean
   /** 题目总数 */
   totalQuestions: number | null
   /** 已完成题目数 */
@@ -757,3 +763,65 @@ export interface UserQuestionListResponseDTO {
   /** 考核是否已结束 */
   ended: boolean
 }
+
+/** 考核队伍成员信息 - 对应后端 AssessmentTeamMemberDTO */
+export interface AssessmentTeamMemberDTO {
+  /** 用户ID */
+  userId: number
+  /** 用户名 */
+  username: string
+  /** 昵称 */
+  nickname: string | null
+  /** 方向 */
+  direction: Direction | null
+  /** 是否为队长 */
+  leader: boolean
+}
+
+/** 考核队伍信息 - 对应后端 AssessmentTeamDTO */
+export interface AssessmentTeamDTO {
+  /** 队伍ID */
+  id: number
+  /** 队伍名称 */
+  name: string
+  /** 考核时间ID */
+  assessmentTimeId: number
+  /** 队长ID */
+  leaderId: number
+  /** 队长名称 */
+  leaderName: string
+  /** 邀请码 */
+  inviteCode: string
+  /** 成员列表 */
+  members: AssessmentTeamMemberDTO[]
+  /** 创建时间 */
+  createdAt: string
+}
+
+/** 创建队伍请求 - 对应后端 CreateAssessmentTeamRequestDTO */
+export interface CreateAssessmentTeamRequestDTO {
+  /** 考核时间ID */
+  assessmentTimeId: number
+  /** 队伍名称 */
+  name: string
+}
+
+/** 加入队伍请求 - 对应后端 JoinAssessmentTeamRequestDTO */
+export interface JoinAssessmentTeamRequestDTO {
+  /** 邀请码 */
+  inviteCode: string
+}
+
+/** 转让队长请求 - 对应后端 TransferLeaderRequestDTO */
+export interface TransferLeaderRequestDTO {
+  /** 队伍ID */
+  teamId: number
+  /** 新队长用户ID */
+  newLeaderId: number
+}
+
+/** 退出队伍请求 - 对应后端 LeaveTeamRequestDTO */
+export interface LeaveTeamRequestDTO {
+  /** 队伍ID */
+  teamId: number
+}
diff --git a/src/frontend/src/apis/services/assessment-team.service.ts b/src/frontend/src/apis/services/assessment-team.service.ts
new file mode 100644
index 0000000..25d6ea1
--- /dev/null
+++ b/src/frontend/src/apis/services/assessment-team.service.ts
@@ -0,0 +1,99 @@
+import { apiClient } from '../client'
+import { ResponseMessage } from '../schema/type'
+import type {
+  AssessmentTeamDTO,
+  CreateAssessmentTeamRequestDTO,
+  JoinAssessmentTeamRequestDTO,
+  TransferLeaderRequestDTO,
+  LeaveTeamRequestDTO,
+} from '@/apis/schema/assessment.dto'
+
+/**
+ * 考核队伍服务 API
+ * 对应后端 /api/v1/assessment-teams/* 接口
+ */
+export const assessmentTeamService = {
+  /**
+   * 创建队伍
+   * POST /api/v1/assessment-teams
+   */
+  async createTeam(
+    request: CreateAssessmentTeamRequestDTO
+  ): Promise<ResponseMessage<AssessmentTeamDTO>> {
+    const response = await apiClient.post<ResponseMessage<AssessmentTeamDTO>>(
+      '/assessment-teams',
+      request
+    )
+    return response.data
+  },
+
+  /**
+   * 预览队伍（通过邀请码）
+   * POST /api/v1/assessment-teams/preview
+   */
+  async previewTeam(inviteCode: string): Promise<ResponseMessage<AssessmentTeamDTO>> {
+    const response = await apiClient.post<ResponseMessage<AssessmentTeamDTO>>(
+      '/assessment-teams/preview',
+      { inviteCode }
+    )
+    return response.data
+  },
+
+  /**
+   * 加入队伍
+   * POST /api/v1/assessment-teams/join
+   */
+  async joinTeam(
+    request: JoinAssessmentTeamRequestDTO
+  ): Promise<ResponseMessage<AssessmentTeamDTO>> {
+    const response = await apiClient.post<ResponseMessage<AssessmentTeamDTO>>(
+      '/assessment-teams/join',
+      request
+    )
+    return response.data
+  },
+
+  /**
+   * 获取我的队伍
+   * GET /api/v1/assessment-teams/my-team?assessmentTimeId={id}
+   */
+  async getMyTeam(assessmentTimeId: number): Promise<ResponseMessage<AssessmentTeamDTO | null>> {
+    const response = await apiClient.get<ResponseMessage<AssessmentTeamDTO | null>>(
+      '/assessment-teams/my-team',
+      { params: { assessmentTimeId } }
+    )
+    return response.data
+  },
+
+  /**
+   * 退出队伍
+   * POST /api/v1/assessment-teams/leave
+   */
+  async leaveTeam(request: LeaveTeamRequestDTO): Promise<ResponseMessage<void>> {
+    const response = await apiClient.post<ResponseMessage<void>>('/assessment-teams/leave', request)
+    return response.data
+  },
+
+  /**
+   * 转让队长
+   * POST /api/v1/assessment-teams/transfer
+   */
+  async transferLeader(
+    request: TransferLeaderRequestDTO
+  ): Promise<ResponseMessage<AssessmentTeamDTO>> {
+    const response = await apiClient.post<ResponseMessage<AssessmentTeamDTO>>(
+      '/assessment-teams/transfer',
+      request
+    )
+    return response.data
+  },
+
+  /**
+   * 解散队伍
+   * DELETE /api/v1/assessment-teams/{id}
+   */
+  async disbandTeam(teamId: number): Promise<ResponseMessage<void>> {
+    const response = await apiClient.delete<ResponseMessage<void>>(`/assessment-teams/${teamId}`)
+    return response.data
+  },
+}
diff --git a/src/frontend/src/app/(public)/(other)/assessment/[timeId]/questions/page.tsx b/src/frontend/src/app/(public)/(other)/assessment/[timeId]/questions/page.tsx
index 5402300..d8f24dc 100644
--- a/src/frontend/src/app/(public)/(other)/assessment/[timeId]/questions/page.tsx
+++ b/src/frontend/src/app/(public)/(other)/assessment/[timeId]/questions/page.tsx
@@ -9,16 +9,21 @@ import {
   MinusCircleOutlined,
   FileTextOutlined,
   TrophyOutlined,
+  TeamOutlined,
+  PlusOutlined,
+  LoginOutlined,
 } from '@ant-design/icons'
-import { Spin, Table, Tag, message } from 'antd'
+import { Spin, Table, Tag, message, Button, Modal, Input, Form } from 'antd'
 import type { TableColumnsType } from 'antd'
 import { assessmentQuestionService } from '@/apis/services/assessment-question.service'
 import { assessmentTimeService } from '@/apis/services/assessment-time.service'
+import { assessmentTeamService } from '@/apis/services/assessment-team.service'
 import { useAuth } from '@/hooks'
 import type {
   AssessmentQuestionDTO,
   AssessmentTimeDTO,
   QuestionType,
+  AssessmentTeamDTO,
 } from '@/apis/schema/assessment.dto'
 import { QuestionTypeLabels } from '@/types/assessment'
 import { DIRECTION_LABELS as DirectionLabels } from '@/apis/schema/enumerate'
@@ -74,7 +79,14 @@ export default function QuestionsPage() {
   const [totalElements, setTotalElements] = useState(0)
   const [ended, setEnded] = useState(false)
   const [loading, setLoading] = useState(true)
-  const { isAuthenticated, checkAuthStatus } = useAuth()
+  const [teamInfo, setTeamInfo] = useState<AssessmentTeamDTO | null>(null)
+  const [teamLoading, setTeamLoading] = useState(false)
+  const [createTeamModalOpen, setCreateTeamModalOpen] = useState(false)
+  const [joinTeamModalOpen, setJoinTeamModalOpen] = useState(false)
+  const [createTeamForm] = Form.useForm()
+  const [joinTeamForm] = Form.useForm()
+  const [teamActionLoading, setTeamActionLoading] = useState(false)
+  const { isAuthenticated, checkAuthStatus, userInfo } = useAuth()
 
   // 认证检查
   useEffect(() => {
@@ -119,6 +131,22 @@ export default function QuestionsPage() {
     }
   }, [timeId, currentPage])
 
+  // 加载队伍信息
+  const fetchTeamInfo = useCallback(async () => {
+    if (!timeInfo?.allowTeam) return
+    setTeamLoading(true)
+    try {
+      const response = await assessmentTeamService.getMyTeam(timeId)
+      if (response.code === 200) {
+        setTeamInfo(response.data)
+      }
+    } catch (error) {
+      console.error('Failed to fetch team info:', error)
+    } finally {
+      setTeamLoading(false)
+    }
+  }, [timeId, timeInfo?.allowTeam])
+
   useEffect(() => {
     if (isAuthenticated) {
       fetchTimeInfo()
@@ -126,6 +154,64 @@ export default function QuestionsPage() {
     }
   }, [isAuthenticated, fetchTimeInfo, fetchQuestions])
 
+  // 考核时间信息加载完成后，加载队伍信息
+  useEffect(() => {
+    if (isAuthenticated && timeInfo?.allowTeam) {
+      fetchTeamInfo()
+    }
+  }, [isAuthenticated, timeInfo?.allowTeam, fetchTeamInfo])
+
+  // 创建队伍
+  const handleCreateTeam = async () => {
+    try {
+      const values = await createTeamForm.validateFields()
+      setTeamActionLoading(true)
+      const response = await assessmentTeamService.createTeam({
+        assessmentTimeId: timeId,
+        name: values.name,
+      })
+      if (response.code === 200 && response.data) {
+        setTeamInfo(response.data)
+        setCreateTeamModalOpen(false)
+        createTeamForm.resetFields()
+        message.success('队伍创建成功')
+      } else {
+        message.error(response.msg || '创建失败')
+      }
+    } catch (err: unknown) {
+      if (err && typeof err === 'object' && 'errorFields' in err) return
+      const msg = (err as { response?: { data?: { msg?: string } } })?.response?.data?.msg
+      message.error(msg || '创建失败')
+    } finally {
+      setTeamActionLoading(false)
+    }
+  }
+
+  // 加入队伍
+  const handleJoinTeam = async () => {
+    try {
+      const values = await joinTeamForm.validateFields()
+      setTeamActionLoading(true)
+      const response = await assessmentTeamService.joinTeam({
+        inviteCode: values.inviteCode,
+      })
+      if (response.code === 200 && response.data) {
+        setTeamInfo(response.data)
+        setJoinTeamModalOpen(false)
+        joinTeamForm.resetFields()
+        message.success('加入队伍成功')
+      } else {
+        message.error(response.msg || '加入失败')
+      }
+    } catch (err: unknown) {
+      if (err && typeof err === 'object' && 'errorFields' in err) return
+      const msg = (err as { response?: { data?: { msg?: string } } })?.response?.data?.msg
+      message.error(msg || '加入失败')
+    } finally {
+      setTeamActionLoading(false)
+    }
+  }
+
   const columns: TableColumnsType<AssessmentQuestionDTO> = useMemo(
     () => [
       {
@@ -256,9 +342,73 @@ export default function QuestionsPage() {
                       {formatDate(timeInfo.startTime)} — {formatDate(timeInfo.endTime)}
                     </span>
                   </span>
+                  {timeInfo.allowTeam && (
+                    <Tag color="blue" icon={<TeamOutlined />}>
+                      允许组队
+                    </Tag>
+                  )}
                 </>
               )}
             </div>
+
+            {/* 队伍信息区域 */}
+            {timeInfo?.allowTeam && !ended && (
+              <div className="mb-6 p-4 rounded-xl bg-white/[0.04] border border-white/[0.08] backdrop-blur-xl">
+                {teamLoading ? (
+                  <div className="flex items-center gap-2 text-white/45">
+                    <Spin size="small" />
+                    <span className="text-[13px]">加载队伍信息...</span>
+                  </div>
+                ) : teamInfo ? (
+                  <div className="flex items-center justify-between flex-wrap gap-3">
+                    <div className="flex items-center gap-3">
+                      <div className="w-9 h-9 rounded-lg bg-[#6677ff]/[0.15] flex items-center justify-center">
+                        <TeamOutlined className="text-lg text-[#6677ff]" />
+                      </div>
+                      <div className="flex flex-col">
+                        <span className="text-sm font-medium text-white">{teamInfo.name}</span>
+                        <span className="text-[12px] text-white/45">
+                          队长：{teamInfo.leaderName} · 成员 {teamInfo.members.length} 人
+                        </span>
+                      </div>
+                    </div>
+                    <Button
+                      type="primary"
+                      size="small"
+                      onClick={() =>
+                        router.push(`/assessment/${timeId}/questions/${questions[0]?.id || ''}`)
+                      }
+                    >
+                      进入答题
+                    </Button>
+                  </div>
+                ) : (
+                  <div className="flex items-center justify-between flex-wrap gap-3">
+                    <div className="flex items-center gap-2 text-white/45">
+                      <TeamOutlined className="text-sm" />
+                      <span className="text-[13px]">本考核允许组队，您当前未加入队伍</span>
+                    </div>
+                    <div className="flex gap-2">
+                      <Button
+                        type="primary"
+                        size="small"
+                        icon={<PlusOutlined />}
+                        onClick={() => setCreateTeamModalOpen(true)}
+                      >
+                        创建队伍
+                      </Button>
+                      <Button
+                        size="small"
+                        icon={<LoginOutlined />}
+                        onClick={() => setJoinTeamModalOpen(true)}
+                      >
+                        加入队伍
+                      </Button>
+                    </div>
+                  </div>
+                )}
+              </div>
+            )}
           </div>
         </div>
 
@@ -330,6 +480,54 @@ export default function QuestionsPage() {
             )}
           </>
         )}
+
+        {/* 创建队伍弹窗 */}
+        <Modal
+          title="创建队伍"
+          open={createTeamModalOpen}
+          onOk={handleCreateTeam}
+          onCancel={() => {
+            setCreateTeamModalOpen(false)
+            createTeamForm.resetFields()
+          }}
+          confirmLoading={teamActionLoading}
+          okText="创建"
+          cancelText="取消"
+        >
+          <Form form={createTeamForm} layout="vertical">
+            <Form.Item
+              name="name"
+              label="队伍名称"
+              rules={[{ required: true, message: '请输入队伍名称' }]}
+            >
+              <Input placeholder="请输入队伍名称" maxLength={30} showCount />
+            </Form.Item>
+          </Form>
+        </Modal>
+
+        {/* 加入队伍弹窗 */}
+        <Modal
+          title="加入队伍"
+          open={joinTeamModalOpen}
+          onOk={handleJoinTeam}
+          onCancel={() => {
+            setJoinTeamModalOpen(false)
+            joinTeamForm.resetFields()
+          }}
+          confirmLoading={teamActionLoading}
+          okText="加入"
+          cancelText="取消"
+        >
+          <Form form={joinTeamForm} layout="vertical">
+            <Form.Item
+              name="inviteCode"
+              label="邀请码"
+              rules={[{ required: true, message: '请输入邀请码' }]}
+            >
+              <Input placeholder="请输入队伍邀请码" />
+            </Form.Item>
+          </Form>
+        </Modal>
       </div>
     </div>
   )
diff --git a/src/frontend/src/app/admin/assessment/time/AssessmentTimeDrawer.tsx b/src/frontend/src/app/admin/assessment/time/AssessmentTimeDrawer.tsx
index f319851..ab50e65 100644
--- a/src/frontend/src/app/admin/assessment/time/AssessmentTimeDrawer.tsx
+++ b/src/frontend/src/app/admin/assessment/time/AssessmentTimeDrawer.tsx
@@ -33,6 +33,7 @@ interface FormValues {
   timeRange: [Dayjs, Dayjs]
   timeLimit: boolean
   timeLimitMinutes: number | null
+  allowTeam: boolean
 }
 
 export default function AssessmentTimeDrawer({
@@ -71,6 +72,7 @@ export default function AssessmentTimeDrawer({
         timeRange: [dayjs(assessmentTime.startTime), dayjs(assessmentTime.endTime)],
         timeLimit: assessmentTime.timeLimit,
         timeLimitMinutes: assessmentTime.timeLimitMinutes,
+        allowTeam: assessmentTime.allowTeam,
       })
     }
   }, [open, mode, assessmentTime, form, isCreateMode, isSuperAdmin, userDirection])
@@ -96,6 +98,7 @@ export default function AssessmentTimeDrawer({
         endTime: values.timeRange[1].format('YYYY-MM-DDTHH:mm:ss'),
         timeLimit: values.timeLimit,
         timeLimitMinutes: values.timeLimit ? values.timeLimitMinutes : null,
+        allowTeam: values.allowTeam,
       }
 
       if (isCreateMode) {
@@ -155,7 +158,7 @@ export default function AssessmentTimeDrawer({
         form={form}
         layout="vertical"
         disabled={isViewMode}
-        initialValues={{ timeLimit: false }}
+        initialValues={{ timeLimit: false, allowTeam: false }}
       >
         <Form.Item
           name="direction"
@@ -203,6 +206,10 @@ export default function AssessmentTimeDrawer({
             <InputNumber min={1} placeholder="限时分钟数" className="w-full" suffix="分钟" />
           </Form.Item>
         )}
+
+        <Form.Item name="allowTeam" label="允许组队" valuePropName="checked">
+          <Switch checkedChildren="允许" unCheckedChildren="不允许" />
+        </Form.Item>
       </Form>
     </Drawer>
   )
diff --git a/src/frontend/src/app/admin/assessment/time/page.tsx b/src/frontend/src/app/admin/assessment/time/page.tsx
index ffae35c..2a82411 100644
--- a/src/frontend/src/app/admin/assessment/time/page.tsx
+++ b/src/frontend/src/app/admin/assessment/time/page.tsx
@@ -16,7 +16,7 @@ import {
   Table,
   Tag,
 } from 'antd'
-import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
+import { PlusOutlined, EditOutlined, DeleteOutlined, TeamOutlined } from '@ant-design/icons'
 import type { ColumnsType } from 'antd/es/table'
 import dayjs from 'dayjs'
 import type {
@@ -191,6 +191,19 @@ export default function AssessmentTimeManagementPage() {
         render: (_: unknown, record: AssessmentTimeDTO) =>
           record.timeLimit ? `${record.timeLimitMinutes} 分钟` : '不限时',
       },
+      {
+        title: '组队',
+        key: 'allowTeam',
+        width: 80,
+        render: (_: unknown, record: AssessmentTimeDTO) =>
+          record.allowTeam ? (
+            <Tag color="blue" icon={<TeamOutlined />} bordered={false}>
+              允许
+            </Tag>
+          ) : (
+            <Tag bordered={false}>不允许</Tag>
+          ),
+      },
       {
         title: '状态',
         key: 'status',
@@ -239,7 +252,7 @@ export default function AssessmentTimeManagementPage() {
 
     // Hide some columns on mobile
     if (isMobile) {
-      return cols.filter((c) => !['grade', 'timeLimit'].includes(c.key as string))
+      return cols.filter((c) => !['grade', 'timeLimit', 'allowTeam'].includes(c.key as string))
     }
 
     return cols
diff --git a/src/frontend/src/components/Assessment/AssessmentCard/index.tsx b/src/frontend/src/components/Assessment/AssessmentCard/index.tsx
index de7a146..6b0bbc4 100644
--- a/src/frontend/src/components/Assessment/AssessmentCard/index.tsx
+++ b/src/frontend/src/components/Assessment/AssessmentCard/index.tsx
@@ -8,6 +8,7 @@ import {
   InboxOutlined,
   DesktopOutlined,
   RightOutlined,
+  TeamOutlined,
 } from '@ant-design/icons'
 import type { Assessment } from '@/types/profile'
 import type { AssessmentTimeDTO, AssessmentStatus } from '@/apis/schema/assessment.dto'
@@ -73,6 +74,7 @@ export default function AssessmentCard({ assessment, status }: AssessmentCardPro
   const direction = isDTO ? assessment.direction : null
   const timeLimit = isDTO ? assessment.timeLimit : false
   const timeLimitMinutes = isDTO ? assessment.timeLimitMinutes : undefined
+  const allowTeam = isDTO ? assessment.allowTeam : false
 
   return (
     <div
@@ -153,6 +155,12 @@ export default function AssessmentCard({ assessment, status }: AssessmentCardPro
             <span>不限时</span>
           </div>
         )}
+        {allowTeam && (
+          <div className="flex items-center gap-[6px] text-[13px] text-[#6677ff] font-medium">
+            <TeamOutlined className="text-sm" />
+            <span>允许组队</span>
+          </div>
+        )}
       </div>
 
       {total > 0 && (
diff --git a/src/frontend/src/components/Assessment/QuestionDetail/TeamPanel.tsx b/src/frontend/src/components/Assessment/QuestionDetail/TeamPanel.tsx
new file mode 100644
index 0000000..0658bf9
--- /dev/null
+++ b/src/frontend/src/components/Assessment/QuestionDetail/TeamPanel.tsx
@@ -0,0 +1,246 @@
+'use client'
+
+import { useState } from 'react'
+import {
+  TeamOutlined,
+  CrownOutlined,
+  CopyOutlined,
+  LogoutOutlined,
+  UserSwitchOutlined,
+  DeleteOutlined,
+  CheckCircleOutlined,
+} from '@ant-design/icons'
+import { Button, Tag, Modal, Select, message, Tooltip } from 'antd'
+import type { AssessmentTeamDTO, AssessmentTeamMemberDTO } from '@/apis/schema/assessment.dto'
+import { DIRECTION_LABELS } from '@/apis/schema/enumerate'
+
+interface TeamPanelProps {
+  team: AssessmentTeamDTO
+  currentUserId: number
+  onLeaveTeam: () => void
+  onTransferLeader: (newLeaderId: number) => void
+  onDisbandTeam: () => void
+  loading?: boolean
+}
+
+export default function TeamPanel({
+  team,
+  currentUserId,
+  onLeaveTeam,
+  onTransferLeader,
+  onDisbandTeam,
+  loading,
+}: TeamPanelProps) {
+  const isLeader = team.leaderId === currentUserId
+  const [leaveModalOpen, setLeaveModalOpen] = useState(false)
+  const [transferModalOpen, setTransferModalOpen] = useState(false)
+  const [disbandModalOpen, setDisbandModalOpen] = useState(false)
+  const [selectedNewLeader, setSelectedNewLeader] = useState<number | null>(null)
+  const [copied, setCopied] = useState(false)
+
+  const handleCopyInviteCode = async () => {
+    try {
+      await navigator.clipboard.writeText(team.inviteCode)
+      setCopied(true)
+      message.success('邀请码已复制')
+      setTimeout(() => setCopied(false), 2000)
+    } catch {
+      message.error('复制失败')
+    }
+  }
+
+  const otherMembers = team.members.filter((m) => m.userId !== team.leaderId)
+  const leaderMember = team.members.find((m) => m.leader)
+
+  const renderMember = (member: AssessmentTeamMemberDTO) => (
+    <div
+      key={member.userId}
+      className="flex items-center gap-2.5 py-2 px-3 rounded-lg bg-white/[0.04]"
+    >
+      <div className="w-7 h-7 rounded-full bg-[#6677ff]/[0.15] flex items-center justify-center text-[11px] text-[#6677ff] font-medium shrink-0">
+        {member.username.charAt(0)}
+      </div>
+      <div className="flex-1 min-w-0">
+        <div className="flex items-center gap-1.5">
+          <span className="text-[13px] text-white truncate">{member.username}</span>
+          {member.leader && (
+            <Tag color="gold" className="!text-[10px] !px-1 !py-0 !leading-4">
+              <CrownOutlined className="text-[10px] mr-0.5" />
+              队长
+            </Tag>
+          )}
+        </div>
+        {member.direction && (
+          <span className="text-[11px] text-white/35">
+            {DIRECTION_LABELS[member.direction] || member.direction}
+          </span>
+        )}
+      </div>
+    </div>
+  )
+
+  return (
+    <div className="bg-white/[0.06] border border-white/[0.08] rounded-xl p-5 flex flex-col gap-4">
+      <div className="flex items-center justify-between">
+        <div className="flex items-center gap-2">
+          <TeamOutlined className="text-base text-[#6677ff]" />
+          <span className="text-sm font-semibold text-white">我的队伍</span>
+        </div>
+        {isLeader && (
+          <Tag color="gold" className="!text-[10px] !px-1.5 !py-0 !leading-5">
+            <CrownOutlined className="text-[10px] mr-0.5" />
+            队长
+          </Tag>
+        )}
+      </div>
+
+      <hr className="w-full h-px bg-white/[0.04] border-none m-0" />
+
+      {/* 队伍名称 */}
+      <div className="flex items-center justify-between">
+        <span className="text-[13px] text-white/45">队伍名称</span>
+        <span className="text-[13px] text-white font-medium">{team.name}</span>
+      </div>
+
+      {/* 邀请码（仅队长可见） */}
+      {isLeader && (
+        <div className="flex items-center justify-between">
+          <span className="text-[13px] text-white/45">邀请码</span>
+          <div className="flex items-center gap-2">
+            <code className="text-[13px] text-[#6677ff] bg-[#6677ff]/[0.08] px-2 py-0.5 rounded font-mono">
+              {team.inviteCode}
+            </code>
+            <Tooltip title={copied ? '已复制' : '复制邀请码'}>
+              <button
+                className="w-6 h-6 rounded flex items-center justify-center bg-white/[0.06] border-none cursor-pointer transition-colors hover:bg-white/[0.1]"
+                onClick={handleCopyInviteCode}
+              >
+                {copied ? (
+                  <CheckCircleOutlined className="text-[11px] text-[#07c160]" />
+                ) : (
+                  <CopyOutlined className="text-[11px] text-white/45" />
+                )}
+              </button>
+            </Tooltip>
+          </div>
+        </div>
+      )}
+
+      {/* 成员列表 */}
+      <div className="flex flex-col gap-1.5">
+        <span className="text-[13px] text-white/45 mb-1">成员 ({team.members.length} 人)</span>
+        <div className="flex flex-col gap-1.5 max-h-[200px] overflow-y-auto">
+          {leaderMember && renderMember(leaderMember)}
+          {otherMembers.map(renderMember)}
+        </div>
+      </div>
+
+      {/* 操作按钮 */}
+      <div className="flex flex-col gap-2 mt-1">
+        {isLeader ? (
+          <>
+            <Button
+              size="small"
+              icon={<UserSwitchOutlined />}
+              onClick={() => {
+                setSelectedNewLeader(null)
+                setTransferModalOpen(true)
+              }}
+              className="!text-[13px]"
+            >
+              转让队长
+            </Button>
+            <Button
+              size="small"
+              danger
+              icon={<DeleteOutlined />}
+              onClick={() => setDisbandModalOpen(true)}
+              className="!text-[13px]"
+            >
+              解散队伍
+            </Button>
+          </>
+        ) : (
+          <Button
+            size="small"
+            danger
+            icon={<LogoutOutlined />}
+            onClick={() => setLeaveModalOpen(true)}
+            className="!text-[13px]"
+          >
+            退出队伍
+          </Button>
+        )}
+      </div>
+
+      {/* 退出队伍确认 */}
+      <Modal
+        title="确认退出队伍"
+        open={leaveModalOpen}
+        onOk={() => {
+          setLeaveModalOpen(false)
+          onLeaveTeam()
+        }}
+        onCancel={() => setLeaveModalOpen(false)}
+        confirmLoading={loading}
+        okText="确认退出"
+        cancelText="取消"
+        okButtonProps={{ danger: true }}
+      >
+        <p>确定要退出队伍「{team.name}」吗？</p>
+      </Modal>
+
+      {/* 转让队长 */}
+      <Modal
+        title="转让队长"
+        open={transferModalOpen}
+        onOk={() => {
+          if (!selectedNewLeader) {
+            message.warning('请选择新队长')
+            return
+          }
+          setTransferModalOpen(false)
+          onTransferLeader(selectedNewLeader)
+          setSelectedNewLeader(null)
+        }}
+        onCancel={() => {
+          setTransferModalOpen(false)
+          setSelectedNewLeader(null)
+        }}
+        confirmLoading={loading}
+        okText="确认转让"
+        cancelText="取消"
+      >
+        <p className="text-white/65 mb-4">请选择新的队长：</p>
+        <Select
+          className="w-full"
+          placeholder="选择新队长"
+          value={selectedNewLeader}
+          onChange={setSelectedNewLeader}
+          options={otherMembers.map((m) => ({
+            value: m.userId,
+            label: `${m.username}${m.nickname ? ` (${m.nickname})` : ''}`,
+          }))}
+        />
+      </Modal>
+
+      {/* 解散队伍确认 */}
+      <Modal
+        title="确认解散队伍"
+        open={disbandModalOpen}
+        onOk={() => {
+          setDisbandModalOpen(false)
+          onDisbandTeam()
+        }}
+        onCancel={() => setDisbandModalOpen(false)}
+        confirmLoading={loading}
+        okText="确认解散"
+        cancelText="取消"
+        okButtonProps={{ danger: true }}
+      >
+        <p>确定要解散队伍「{team.name}」吗？此操作不可撤销。</p>
+        <p className="text-white/45 text-[13px] mt-2">队伍解散后，所有成员将需要重新组队。</p>
+      </Modal>
+    </div>
+  )
+}
diff --git a/src/frontend/src/components/Assessment/QuestionDetail/index.tsx b/src/frontend/src/components/Assessment/QuestionDetail/index.tsx
index 2f65bab..cc5f5af 100644
--- a/src/frontend/src/components/Assessment/QuestionDetail/index.tsx
+++ b/src/frontend/src/components/Assessment/QuestionDetail/index.tsx
@@ -11,12 +11,15 @@ import {
   UploadOutlined,
   ExperimentOutlined,
   CheckCircleOutlined,
+  TeamOutlined,
+  PlusOutlined,
 } from '@ant-design/icons'
 import { Button, Tag, message, Spin, Upload, type UploadProps } from 'antd'
 import { assessmentQuestionService } from '@/apis/services/assessment-question.service'
 import { assessmentTimeService } from '@/apis/services/assessment-time.service'
 import { assessmentAnswerService } from '@/apis/services/assessment-answer.service'
 import { assessmentSessionService } from '@/apis/services/assessment-session.service'
+import { assessmentTeamService } from '@/apis/services/assessment-team.service'
 import { algorithmJudgeService } from '@/apis/services/algorithm-judge.service'
 import { assessmentStatisticsService } from '@/apis/services/assessment-statistics.service'
 import { fileService } from '@/apis/services/file.service'
@@ -33,6 +36,7 @@ import type {
   JudgeJobPollingResponseDTO,
   ProgrammingLanguage,
   QuestionStatisticsDTO,
+  AssessmentTeamDTO,
 } from '@/apis/schema/assessment.dto'
 import { DIRECTION_LABELS as DirectionLabels } from '@/apis/schema/enumerate'
 import { QuestionTypeLabels } from '@/types/assessment'
@@ -43,6 +47,7 @@ import AlgorithmQuestion from './AlgorithmQuestion'
 import JudgeResultPanel from './JudgeResultPanel'
 import QuestionSidebar from './QuestionSidebar'
 import CountdownSection from './CountdownSection'
+import TeamPanel from './TeamPanel'
 import styles from '@/app/(public)/(other)/assessment/[timeId]/questions/[questionId]/styles.module.css'
 import { getStatusInfo, formatFileSize, getUploadPhase } from './utils'
 import { LANGUAGE_LABELS } from './constants'
@@ -76,8 +81,10 @@ export default function QuestionDetailPage() {
   const [questionStatistics, setQuestionStatistics] = useState<QuestionStatisticsDTO | null>(null)
   const [pollingJobId, setPollingJobId] = useState<number | null>(null)
   const [pollingFormalJob, setPollingFormalJob] = useState(false)
+  const [teamInfo, setTeamInfo] = useState<AssessmentTeamDTO | null>(null)
+  const [teamLoading, setTeamLoading] = useState(false)
   const autoSubmitRef = useRef(false)
-  const { isAuthenticated, checkAuthStatus } = useAuth()
+  const { isAuthenticated, checkAuthStatus, userInfo } = useAuth()
 
   // 认证检查
   useEffect(() => {
@@ -155,6 +162,22 @@ export default function QuestionDetailPage() {
     }
   }, [questionId])
 
+  // 加载队伍信息
+  const fetchTeamInfo = useCallback(async () => {
+    if (!timeInfo?.allowTeam) return
+    setTeamLoading(true)
+    try {
+      const response = await assessmentTeamService.getMyTeam(timeId)
+      if (response.code === 200) {
+        setTeamInfo(response.data)
+      }
+    } catch (error) {
+      console.error('Failed to fetch team info:', error)
+    } finally {
+      setTeamLoading(false)
+    }
+  }, [timeId, timeInfo?.allowTeam])
+
   // 后端未开启候选人通过率展示时会返回错误，这里静默隐藏可选统计卡片
   const fetchQuestionStatistics = useCallback(async () => {
     try {
@@ -194,6 +217,13 @@ export default function QuestionDetailPage() {
     fetchSession,
   ])
 
+  // timeInfo 加载完成后获取队伍信息
+  useEffect(() => {
+    if (isAuthenticated && timeInfo?.allowTeam && !loading) {
+      fetchTeamInfo()
+    }
+  }, [isAuthenticated, timeInfo?.allowTeam, loading, fetchTeamInfo])
+
   // 非限时考核：endTime 到达时自动标记过期
   useEffect(() => {
     if (!timeInfo || timeInfo.timeLimit || !timeInfo.endTime) return
@@ -519,6 +549,64 @@ export default function QuestionDetailPage() {
     }
   }
 
+  // 队伍管理操作
+  const handleLeaveTeam = async () => {
+    if (!teamInfo) return
+    setTeamLoading(true)
+    try {
+      const response = await assessmentTeamService.leaveTeam({ teamId: teamInfo.id })
+      if (response.code === 200) {
+        setTeamInfo(null)
+        message.success('已退出队伍')
+      } else {
+        message.error(response.msg || '退出失败')
+      }
+    } catch (error) {
+      message.error('退出失败')
+    } finally {
+      setTeamLoading(false)
+    }
+  }
+
+  const handleTransferLeader = async (newLeaderId: number) => {
+    if (!teamInfo) return
+    setTeamLoading(true)
+    try {
+      const response = await assessmentTeamService.transferLeader({
+        teamId: teamInfo.id,
+        newLeaderId,
+      })
+      if (response.code === 200 && response.data) {
+        setTeamInfo(response.data)
+        message.success('队长转让成功')
+      } else {
+        message.error(response.msg || '转让失败')
+      }
+    } catch (error) {
+      message.error('转让失败')
+    } finally {
+      setTeamLoading(false)
+    }
+  }
+
+  const handleDisbandTeam = async () => {
+    if (!teamInfo) return
+    setTeamLoading(true)
+    try {
+      const response = await assessmentTeamService.disbandTeam(teamInfo.id)
+      if (response.code === 200) {
+        setTeamInfo(null)
+        message.success('队伍已解散')
+      } else {
+        message.error(response.msg || '解散失败')
+      }
+    } catch (error) {
+      message.error('解散失败')
+    } finally {
+      setTeamLoading(false)
+    }
+  }
+
   // 导航
   const currentIndex = questionsList.findIndex((q) => q.id === questionId)
   const hasPrev = currentIndex > 0
@@ -581,6 +669,14 @@ export default function QuestionDetailPage() {
       ? `${(Number(questionStatistics.passRate) * 100).toFixed(2)}%`
       : null
 
+  // 队伍相关计算
+  const allowTeam = timeInfo?.allowTeam ?? false
+  const isInTeam = teamInfo !== null
+  const isTeamLeader = isInTeam && teamInfo?.leaderId === userInfo?.id
+  const canUploadFile = !allowTeam || isTeamLeader
+  const showTeamPanel = allowTeam && isFileUpload
+  const showTeamActionInUpload = allowTeam && isFileUpload && !isInTeam && !isExpired
+
   const allowedExtsText = fileContent?.allowedExtensions
     ? `支持 ${fileContent.allowedExtensions.join(', ')} 格式`
     : '支持所有文件格式'
@@ -756,19 +852,71 @@ export default function QuestionDetailPage() {
                 </div>
                 <hr className="w-full h-px bg-white/[0.04] border-none m-0" />
                 <div className="flex-1 pt-[18px]">
-                  <FileUploadArea
-                    uploadPhase={uploadPhase}
-                    uploadedFile={uploadedFile}
-                    uploadProgress={uploadProgress}
-                    presignedPhase={presignedPhase}
-                    isExpired={isExpired}
-                    answer={answer}
-                    dropHintText={dropHintText}
-                    draggerProps={draggerProps}
-                    onResubmit={() => setIsResubmitting(true)}
-                    onRemoveFile={handleRemoveFile}
-                    onSetUploadedFile={setUploadedFile}
-                  />
+                  {/* 允许组队但未在队伍中：显示创建/加入队伍按钮 */}
+                  {showTeamActionInUpload ? (
+                    <div className="flex flex-col items-center gap-4 py-8 px-4 rounded-[10px] bg-white/[0.03] border border-white/[0.06]">
+                      <TeamOutlined className="text-[32px] text-[#6677ff]/40" />
+                      <p className="text-[13px] text-white/45 m-0">
+                        本考核允许组队，请先创建或加入队伍
+                      </p>
+                      <div className="flex gap-3">
+                        <Button
+                          type="primary"
+                          icon={<PlusOutlined />}
+                          onClick={() => router.push(`/assessment/${timeId}/questions`)}
+                        >
+                          去创建/加入队伍
+                        </Button>
+                      </div>
+                    </div>
+                  ) : /* 在队伍中但不是队长：只读显示 */
+                  allowTeam && isInTeam && !isTeamLeader ? (
+                    <div className="flex flex-col gap-4">
+                      {answer?.fileId ? (
+                        <div className="flex items-center gap-4 p-5 rounded-[10px] bg-[#07c160]/[0.06] border border-[#07c160]/[0.12]">
+                          <CheckCircleOutlined className="text-[32px] text-[#07c160]" />
+                          <div className="flex-1">
+                            <p className="text-base font-semibold text-[#07c160] mb-1">
+                              队长已提交
+                            </p>
+                            <p className="text-[13px] text-white/45 m-0">
+                              提交时间：
+                              {answer?.submitTime
+                                ? new Date(answer.submitTime).toLocaleString('zh-CN')
+                                : '-'}
+                            </p>
+                          </div>
+                        </div>
+                      ) : (
+                        <div className="flex items-center gap-4 p-5 rounded-[10px] bg-white/[0.03] border border-white/[0.06]">
+                          <TeamOutlined className="text-[32px] text-white/20" />
+                          <div>
+                            <p className="text-base font-semibold text-white/45 mb-1">
+                              等待队长提交
+                            </p>
+                            <p className="text-[13px] text-white/30 m-0">
+                              您无上传权限，请联系队长
+                            </p>
+                          </div>
+                        </div>
+                      )}
+                    </div>
+                  ) : (
+                    /* 普通情况或队长：正常上传 */
+                    <FileUploadArea
+                      uploadPhase={uploadPhase}
+                      uploadedFile={uploadedFile}
+                      uploadProgress={uploadProgress}
+                      presignedPhase={presignedPhase}
+                      isExpired={isExpired}
+                      answer={answer}
+                      dropHintText={dropHintText}
+                      draggerProps={draggerProps}
+                      onResubmit={() => setIsResubmitting(true)}
+                      onRemoveFile={handleRemoveFile}
+                      onSetUploadedFile={setUploadedFile}
+                    />
+                  )}
                 </div>
               </section>
             ) : isChoiceQuestion ? (
@@ -824,6 +972,16 @@ export default function QuestionDetailPage() {
 
           {/* Sidebar */}
           <aside className="w-full lg:w-80 flex-shrink-0 lg:sticky lg:top-6 lg:self-start flex flex-col gap-6">
+            {showTeamPanel && teamInfo && userInfo && (
+              <TeamPanel
+                team={teamInfo}
+                currentUserId={userInfo.id}
+                onLeaveTeam={handleLeaveTeam}
+                onTransferLeader={handleTransferLeader}
+                onDisbandTeam={handleDisbandTeam}
+                loading={teamLoading}
+              />
+            )}
             <CountdownSection
               isTimed={isTimed}
               deadline={deadline}
```

### `03df5666` chore: 删除测试过程产生的cookies文件

- **时间:** 2026-05-16 14:11:44 +0800

**提交信息:**

chore: 删除测试过程产生的cookies文件

**代码变更:**

```diff
diff --git a/src/backend/cookies.txt b/src/backend/cookies.txt
deleted file mode 100644
index fc76254..0000000
--- a/src/backend/cookies.txt
+++ /dev/null
@@ -1,6 +0,0 @@
-# Netscape HTTP Cookie File
-# https://curl.se/docs/http-cookies.html
-# This file was generated by libcurl! Edit at your own risk.
-
-localhost	FALSE	/	FALSE	1778269686	csrf_token	srFKmjhZNX8WSIJZVZoLHZMrweaLE5-OjmLmgYwVyTc
-#HttpOnly_localhost	FALSE	/	FALSE	1778269686	auth_token	eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxIiwianRpIjoiZjUwMzE2N2QtY2YzZi00YWZlLWFmNWQtYTE3OTlkNmQ4YjIzIiwiaWF0IjoxNzc4MjI2NDg1LCJleHAiOjE3NzgyNjk2ODV9.S2_BgCGQIU5kENiOsxJ617D70okqVj_wye1BGtefKes
```

---

## 仓库: `E:\code\code_project\lianji`

### `7dfee0fe` refactor(ui): migrate pages to use Scaffold and adjust window insets

- **时间:** 2026-05-16 22:25:09 +0800

**提交信息:**

refactor(ui): migrate pages to use Scaffold and adjust window insets

1. 为NavHost添加无偏移的窗口Insets配置
2. 将注册页和纪念日列表页重构为使用Scaffold布局
3. 调整FAB的位置逻辑，移除嵌套Scaffold的问题代码
4. 统一页面背景色和内边距的处理方式

**代码变更:**

```diff
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt
index be7d822..578c10c 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt
@@ -29,6 +29,7 @@ import androidx.compose.material3.ExperimentalMaterial3Api
 import androidx.compose.material3.FloatingActionButton
 import androidx.compose.material3.Icon
 import androidx.compose.material3.IconButton
+import androidx.compose.material3.Scaffold
 import androidx.compose.material3.Text
 import androidx.compose.material3.TopAppBar
 import androidx.compose.material3.TopAppBarDefaults
@@ -67,12 +68,9 @@ fun AnniversaryListContent(
     val isRefreshing = uiState is AnniversaryListUiState.Loading
     val swipeRefreshState = rememberSwipeRefreshState(isRefreshing)
 
-    Box(modifier = modifier.fillMaxSize()) {
-        Column(
-            modifier = Modifier
-                .fillMaxSize()
-                .background(BackgroundLight)
-        ) {
+    Scaffold(
+        modifier = modifier,
+        topBar = {
             TopAppBar(
                 title = {
                     Text(
@@ -86,10 +84,33 @@ fun AnniversaryListContent(
                     containerColor = BackgroundLight
                 )
             )
-
+        },
+        floatingActionButton = {
+            if (uiState is AnniversaryListUiState.Success || uiState is AnniversaryListUiState.Empty) {
+                FloatingActionButton(
+                    onClick = { onEvent(AnniversaryListUiEvent.CreateClick) },
+                    containerColor = LovePink,
+                    shape = CircleShape
+                ) {
+                    Icon(
+                        imageVector = Icons.Default.Add,
+                        contentDescription = "添加纪念日",
+                        tint = SurfaceLight
+                    )
+                }
+            }
+        }
+    ) { paddingValues ->
+        Box(
+            modifier = Modifier
+                .fillMaxSize()
+                .padding(paddingValues)
+                .background(BackgroundLight)
+        ) {
             SwipeRefresh(
                 state = swipeRefreshState,
                 onRefresh = { onEvent(AnniversaryListUiEvent.Refresh) },
+                modifier = Modifier.fillMaxSize(),
                 indicator = { state, trigger ->
                     SwipeRefreshIndicator(
                         state = state,
@@ -153,24 +174,6 @@ fun AnniversaryListContent(
                 }
             }
         }
-
-        // FAB positioned absolutely to avoid Scaffold nesting issues
-        if (uiState is AnniversaryListUiState.Success || uiState is AnniversaryListUiState.Empty) {
-            FloatingActionButton(
-                onClick = { onEvent(AnniversaryListUiEvent.CreateClick) },
-                containerColor = LovePink,
-                shape = CircleShape,
-                modifier = Modifier
-                    .align(Alignment.BottomEnd)
-                    .padding(end = 24.dp, bottom = 48.dp)
-            ) {
-                Icon(
-                    imageVector = Icons.Default.Add,
-                    contentDescription = "添加纪念日",
-                    tint = SurfaceLight
-                )
-            }
-        }
     }
 }
 
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/register/RegisterContent.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/register/RegisterContent.kt
index 01b3356..65e3877 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/register/RegisterContent.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/register/RegisterContent.kt
@@ -32,8 +32,10 @@ import androidx.compose.material3.CircularProgressIndicator
 import androidx.compose.material3.ExperimentalMaterial3Api
 import androidx.compose.material3.Icon
 import androidx.compose.material3.IconButton
+import androidx.compose.material3.Scaffold
 import androidx.compose.material3.Text
 import androidx.compose.material3.TopAppBar
+import androidx.compose.material3.TopAppBarDefaults
 import androidx.compose.runtime.Composable
 import androidx.compose.ui.Alignment
 import androidx.compose.ui.Modifier
@@ -67,34 +69,37 @@ fun RegisterContent(
     onNavigateToLogin: () -> Unit,
     onNavigateBack: () -> Unit
 ) {
-    Column(
-        modifier = Modifier
-            .fillMaxSize()
-            .background(BackgroundLight)
-    ) {
-        TopAppBar(
-            title = {
-                Text(
-                    text = "注册",
-                    fontSize = 20.sp,
-                    fontWeight = FontWeight.SemiBold,
-                    color = TextPrimaryLight
-                )
-            },
-            navigationIcon = {
-                IconButton(onClick = onNavigateBack) {
-                    Icon(
-                        imageVector = Icons.AutoMirrored.Filled.ArrowBack,
-                        contentDescription = "返回",
-                        tint = TextPrimaryLight
+    Scaffold(
+        topBar = {
+            TopAppBar(
+                title = {
+                    Text(
+                        text = "注册",
+                        fontSize = 20.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
                     )
-                }
-            }
-        )
-
+                },
+                navigationIcon = {
+                    IconButton(onClick = onNavigateBack) {
+                        Icon(
+                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
+                            contentDescription = "返回",
+                            tint = TextPrimaryLight
+                        )
+                    }
+                },
+                colors = TopAppBarDefaults.topAppBarColors(
+                    containerColor = BackgroundLight
+                )
+            )
+        }
+    ) { paddingValues ->
         Column(
             modifier = Modifier
                 .fillMaxSize()
+                .background(BackgroundLight)
+                .padding(paddingValues)
                 .padding(horizontal = 32.dp)
                 .padding(top = 24.dp, bottom = 32.dp),
             horizontalAlignment = Alignment.CenterHorizontally,
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt b/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
index 6700514..d73433f 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
@@ -7,6 +7,7 @@
 package cn.iven.app.navigation
 
 import android.widget.Toast
+import androidx.compose.foundation.layout.WindowInsets
 import androidx.compose.foundation.layout.padding
 import androidx.compose.material.icons.Icons
 import androidx.compose.material.icons.automirrored.filled.Chat
@@ -101,7 +102,8 @@ fun LianjiNavHost(
                     }
                 }
             }
-        }
+        },
+        contentWindowInsets = WindowInsets(0, 0, 0, 0)
     ) { innerPadding ->
         NavHost(
             navController = navController,
```

### `efea6984` feat: 实现纪念日模块完整功能，新增情侣开始日期管理

- **时间:** 2026-05-16 20:31:54 +0800

**提交信息:**

feat: 实现纪念日模块完整功能，新增情侣开始日期管理

此提交完成了恋记应用纪念日模块的全链路开发：
1. 新增纪念日数据库表与完整领域模型，支持系统级/自定义纪念日、重复类型配置
2. 实现纪念日CRUD、即将到期查询等接口，新增恋爱开始日期修改接口
3. 完成Android端纪念日列表、创建编辑页面与相关导航逻辑
4. 重构登录绑定流程，新增恋爱开始日期设置引导
5. 将首页统计替换为真实业务数据，移除Mock硬编码
6. 绑定成功后自动创建系统级恋爱纪念日

**代码变更:**

```diff
diff --git a/docker/docker-compose.yml b/docker/docker-compose.yml
index c541d92..0fc8ed7 100644
--- a/docker/docker-compose.yml
+++ b/docker/docker-compose.yml
@@ -57,6 +57,7 @@ services:
       DB_USER: postgres
       DB_PASS: ${POSTGRES_PASSWORD}
       REDIS_HOST: redis
+      REDIS_PORT: 6379
       REDIS_PASS: ${REDIS_PASSWORD:-}
       JWT_SECRET: ${JWT_SECRET:-change-me-in-production-please-use-a-long-and-random-string-for-jwt-signing}
       DEBUG: ${DEBUG:-false}
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/.openspec.yaml b/openspec/changes/archive/2026-05-16-anniversary-module/.openspec.yaml
new file mode 100644
index 0000000..ab7f13b
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/.openspec.yaml
@@ -0,0 +1,2 @@
+schema: spec-driven
+created: 2026-05-16
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/design.md b/openspec/changes/archive/2026-05-16-anniversary-module/design.md
new file mode 100644
index 0000000..9c73c0e
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/design.md
@@ -0,0 +1,135 @@
+## Context
+
+恋记项目已完成 Phase 1（基础设施与认证体系），包括：用户注册/登录/登出（JWT + Redis）、情侣绑定（生成绑定码 → 输入绑定码 → 建立关系）、首页 UI（统计卡片 + 时间线 + 纪念日提醒）、DDD 四层架构完整搭建。
+
+当前 `Couple` 实体的 `createdAt` 字段在数据库中默认 `NOW()`，绑定流程中用户无法设置。首页统计 `GET /api/v1/home/stats` 的 `upcomingAnniversaries` 和 `recentMemories` 均为硬编码 Mock 数据。数据库中只有 `app_user` 和 `couple_relationship` 两张表。
+
+本项目采用 DDD 四层架构（API → Application → Domain → Infrastructure）和 Android MVVM + MVI 单向数据流。纪念日是 Phase 2 引入的第一个核心业务领域，其设计将确立后续模块（记事、账本）的架构范式。
+
+## Goals / Non-Goals
+
+**Goals:**
+- 建立独立的 Anniversary 领域，支持系统级与自定义纪念日
+- 实现重复类型计算算法（NONE/YEARLY/MONTHLY），支持闰年 2月29 fallback 到 2月28
+- 首页统计接入真实纪念日数据（`upcomingAnniversaries` + `daysTogether`）
+- 绑定流程补充"设置恋爱开始日期"环节，可跳过，默认用绑定时间
+- 支持修改恋爱开始日期并级联更新系统级纪念日
+
+**Non-Goals:**
+- 消息推送提醒（Phase 4/5 再做，Phase 2 只存 `remindDays` 字段）
+- 记事模块（`recentMemories` 保持 Mock）
+- 纪念日图标/封面图片上传
+- 批量导入/导出纪念日
+- 纪念日分享功能
+
+## Decisions
+
+### 1. 系统级纪念日的数据模型与权限
+
+**决策**：纪念日表统一存储系统级和自定义纪念日，通过 `is_system` 布尔字段区分。
+
+**系统级（当前只有"恋爱开始日"）**：
+- 绑定成功后由后端自动创建
+- 不可删除、不可直接修改日期（改日期走 `PUT /couple/start-date` 级联更新）
+- 可修改标题（允许用户个性化）和提醒天数
+- 固定 `repeat_type = YEARLY`
+
+**自定义纪念日**：
+- 用户通过 `POST /api/v1/anniversaries` 创建
+- 完整 CRUD 权限
+- 支持三种重复类型
+
+**替代方案**：系统级纪念日作为 `Couple` 聚合的内联字段，不在 `anniversary` 表中存储。
+
+**不选原因**：首页"即将到来"和纪念日列表需要统一查询和排序，如果数据分散在两张表，查询复杂度显著增加，且领域边界模糊。
+
+### 2. 恋爱开始日期的权威来源
+
+**决策**：`Couple.createdAt` 是恋爱开始日期的权威来源（source of truth）。系统级纪念日的 `date` 字段是它的投影。
+
+**同步机制**：
+```
+PUT /api/v1/couple/start-date
+  ├── 更新 couple_relationship.created_at
+  └── 级联更新 anniversary 表中 is_system=true 且 couple_id 匹配的记录
+```
+
+**替代方案**：权威来源反过来，由系统级纪念日驱动 Couple 表。
+
+**不选原因**：首页"在一起天数"直接从 `Couple` 计算，如果权威来源在 Anniversary 表，首页统计需要跨聚合查询，破坏 Home 领域的独立性。`Couple.createdAt` 语义上就是"关系开始时间"，不存在数据歧义。
+
+### 3. "即将到来"计算的位置
+
+**决策**："即将到来"的日期计算放在 Application 层（`AnniversaryAppService`），不放在 Domain 层。
+
+**计算逻辑**：
+- `NONE`：计算一次 `date - today`，结果为负则排除
+- `YEARLY`：找到下一个周年日（年份调整为今年，若已过则 +1 年）
+- `MONTHLY`：找到下一个月度日（年月调整为今年今月，若已过则 +1 月）
+- 闰年 2月29 在非闰年 fallback 到 2月28
+
+**替代方案**：放在 Domain 层的 `Anniversary` 实体中作为领域方法。
+
+**不选原因**：计算依赖"当前日期"这个外部上下文。Domain 层应该是时间无关的纯业务逻辑，而"即将到来"本质上是基于查询时点的应用层筛选。
+
+### 4. 系统级纪念日的创建时机
+
+**决策**：绑定成功后在 `CoupleAppService.bind()` 的事务中同步创建系统级纪念日。
+
+**替代方案**：延迟到用户首次访问纪念日列表时再懒创建。
+
+**不选原因**：懒创建会导致边界情况（如用户绑定后立刻进首页，首页调用 `upcomingAnniversaries` 查询时系统级纪念日还不存在）。同步创建保证数据一致性，且事务包裹保证原子性。
+
+### 5. 首页统计与纪念日领域的依赖方向
+
+**决策**：`HomeAppService` 通过接口依赖 `AnniversaryAppService`（应用层服务调用应用层服务）。
+
+**替代方案**：`HomeAppService` 直接依赖 `AnniversaryRepository`（跨领域直接访问仓储）。
+
+**不选原因**：违反 DDD 分层原则。领域仓储是聚合内部的实现细节，跨聚合应该通过应用层服务编排。`AnniversaryAppService` 可以封装"即将到来"的计算逻辑和缓存策略（未来 Phase 5 加 Redis 缓存时只需要改一处）。
+
+### 6. Android 端绑定后日期设置流程
+
+**决策**：绑定成功后由导航层控制流程：`BindScreen` 发出 `BindSuccess` 事件，`NavHost` 判断是否已设置恋爱日期，未设置则弹出日期设置 BottomSheet，已设置则进入首页。
+
+**替代方案**：由 `BindViewModel` 直接决定下一步导航。
+
+**不选原因**：ViewModel 不应该持有导航逻辑（违反 MVVM 中 ViewModel 不依赖 Android 框架的原则）。导航是 UI 层的职责，ViewModel 只应该发出状态变化事件。
+
+## Risks / Trade-offs
+
+**[风险] 已绑定用户缺少系统级纪念日**
+→ **缓解**：现有数据库中已绑定的情侣在部署后没有系统级纪念日记录。方案：
+  1. 提供 Flyway 数据迁移脚本，批量为已有 couple_relationship 创建系统级纪念日（推荐）
+  2. 或应用层在查询时兜底创建（增加查询复杂度，不推荐）
+
+**[风险] 修改恋爱日期导致纪念日列表排序突变**
+→ **缓解**：修改日期是低频操作，用户预期到排序会变化。UI 上在修改成功后可展示 Toast 提示"恋爱日期已更新，纪念日列表已同步"。
+
+**[风险] 应用层服务循环依赖**
+→ **缓解**：`HomeAppService` → `AnniversaryAppService`，`AnniversaryAppService` → `CoupleRepository`（通过 coupleId 验证权限），不存在循环。如未来 `AnniversaryAppService` 需要调用 `HomeAppService`，应通过领域事件解耦。
+
+**[风险] 纪念日数量增长导致"即将到来"查询变慢**
+→ **缓解**：Phase 2 初期情侣的纪念日数量通常 < 50 条，全表扫描无性能问题。Phase 5 可引入 Redis 缓存"即将到来"结果（TTL = 1天），或增加数据库复合索引 `(couple_id, anniversary_date)`。
+
+**[风险] 多设备同时修改恋爱日期导致数据竞争**
+→ **缓解**：`Couple` 表的 `updated_at` 字段配合乐观锁（未来 Phase 5 引入）。Phase 2 暂不做，因为恋爱日期修改是极低频操作，且只有情侣双方有权限。
+
+## Migration Plan
+
+**部署步骤**：
+1. 执行 Flyway V2 迁移脚本创建 `anniversary` 表
+2. 执行数据迁移脚本为已有 couple_relationship 补创建系统级纪念日
+3. 部署后端服务（新 API 上线，首页统计逻辑替换）
+4. 部署 Android App（新版本支持纪念日页面和绑定后引导）
+
+**回滚策略**：
+- 数据库：Flyway 脚本可逆（`DROP TABLE anniversary`），但已有系统级纪念日数据会丢失。回滚前需备份。
+- 后端：首页统计如果出现问题，可临时回退到 Mock 数据版本（修改 `HomeAppServiceImpl`）。
+- Android：新版本兼容旧 API（旧版本不会调用新 API），无需特殊处理。
+
+## Open Questions
+
+1. **数据迁移脚本**：是否需要为已有 couple_relationship 批量创建系统级纪念日？还是仅在应用层首次查询时懒创建？
+2. **纪念日排序规则**："即将到来"按剩余天数升序，如果同一天有多个纪念日，按什么二级排序（创建时间？标题字母序？）
+3. **自定义纪念日的重复类型默认值**：新建纪念日时默认 `NONE` 还是 `YEARLY`？
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/proposal.md b/openspec/changes/archive/2026-05-16-anniversary-module/proposal.md
new file mode 100644
index 0000000..ae8694e
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/proposal.md
@@ -0,0 +1,46 @@
+## Why
+
+首页统计（`GET /api/v1/home/stats`）目前返回全量 Mock 数据，无法真实反映用户的恋爱历程。纪念日模块是恋记 Phase 2 的核心业务领域之一，为用户提供记录恋爱里程碑、查看周年倒计时、管理自定义纪念日的完整能力。同时，绑定流程需要补充"设置恋爱开始日期"环节，让"在一起天数"统计基于用户真实的恋爱起始时间。
+
+## What Changes
+
+**后端变更：**
+- 新增 `anniversary` 数据库表（Flyway V2），支持系统级与自定义纪念日
+- 新增纪念日领域完整链路：Entity → Repository → AppService → Controller + DTO/Converter
+- 实现"即将到来"纪念日查询算法（支持 NONE/YEARLY/MONTHLY 重复类型，闰年 2月29 fallback 到 2月28）
+- 新增 `PUT /api/v1/couple/start-date` 接口，支持修改恋爱开始日期并级联更新系统级纪念日
+- 绑定成功后自动创建系统级纪念日（`is_system=true`，`title="恋爱开始日"`）
+- 首页统计 `GET /api/v1/home/stats` 接入真实数据：
+  - `daysTogether` 基于 `Couple.createdAt`（用户可设置的恋爱开始日期）计算
+  - `upcomingAnniversaries` 从 Anniversary 领域真实查询
+  - `recentMemories` 保持 Mock（等待记事模块完成后替换）
+
+**Android 前端变更：**
+- 新增纪念日列表页：按即将到来天数排序，系统级纪念日特殊标记
+- 新增纪念日创建/编辑页：标题、日期选择、重复类型选择、提醒天数
+- 绑定成功后增加"设置恋爱开始日期"引导弹窗：默认今天，可修改，可跳过
+- 首页"即将到来"卡片接入真实 API 数据
+- "我的"页面增加修改恋爱开始日期入口
+
+**BREAKING：**
+- `HomeAppServiceImpl.getStats()` 将不再返回硬编码 Mock 数据，要求数据库中至少存在 couple_relationship 记录（已有）和 anniversary 记录（绑定后自动创建）。开发环境如直接调用首页接口且未走绑定流程，需要手动插入测试数据。
+
+## Capabilities
+
+### New Capabilities
+- `anniversary-management`: 纪念日 CRUD、系统级与自定义纪念日区分、重复类型计算、即将到来查询
+- `couple-start-date`: 恋爱开始日期设置与修改、绑定后引导流程、级联更新系统级纪念日
+
+### Modified Capabilities
+- `home-stats-api`: 首页统计接口的 `upcomingAnniversaries` 和 `daysTogether` 从 Mock 数据改为真实数据库查询。具体变更：
+  - Requirement "Service layer uses mock data" 将被移除，替换为真实数据查询
+  - Requirement "Upcoming anniversary section" 的实现方式从静态构造改为调用 Anniversary 领域服务
+  - Requirement "Days together calculation" 中的计算基准从系统当前时间隐含的默认值改为用户可设置的 `Couple.createdAt`
+
+## Impact
+
+- **数据库**：新增 `anniversary` 表，新增索引 `idx_anniversary_couple`、`idx_anniversary_date`
+- **后端 API**：新增 5 个接口（纪念日 CRUD + 即将到来查询 + 恋爱日期修改），修改 1 个接口（首页统计）
+- **Android**：新增 2 个页面（纪念日列表、纪念日创建/编辑），修改 2 个页面（绑定流程、首页）
+- **领域依赖**：`HomeAppService` 新增对 `AnniversaryAppService` 和 `CoupleRepository` 的依赖
+- **现有数据**：已绑定情侣的用户在升级后，系统级纪念日将自动补创建（由应用层在首次查询时兜底创建，或通过数据迁移脚本批量创建）
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/specs/anniversary-management/spec.md b/openspec/changes/archive/2026-05-16-anniversary-module/specs/anniversary-management/spec.md
new file mode 100644
index 0000000..77c61bd
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/specs/anniversary-management/spec.md
@@ -0,0 +1,111 @@
+## ADDED Requirements
+
+### Requirement: Anniversary entity supports system and custom types
+The system SHALL store anniversaries with a flag distinguishing system-level records from user-created records.
+
+#### Scenario: System-level anniversary created on couple binding
+- **WHEN** two users successfully bind as a couple
+- **THEN** the system automatically creates an anniversary record with `is_system=true`, `title="恋爱开始日"`, `repeat_type=YEARLY`, and `date` equal to the couple's start date
+
+#### Scenario: Custom anniversary created by user
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with title, date, repeat_type, and optional remind_days
+- **THEN** the system creates an anniversary record with `is_system=false` and returns the created record
+
+### Requirement: System-level anniversary has restricted mutation rules
+The system SHALL enforce different mutation permissions for system-level and custom anniversaries.
+
+#### Scenario: User attempts to delete system-level anniversary
+- **WHEN** an authenticated user sends DELETE /api/v1/anniversaries/{id} for a system-level anniversary
+- **THEN** the system returns HTTP 403 with error code FORBIDDEN
+
+#### Scenario: User modifies system-level anniversary title
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new title for a system-level anniversary
+- **THEN** the system updates the title and returns the updated record
+
+#### Scenario: User attempts to modify system-level anniversary date directly
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new date for a system-level anniversary
+- **THEN** the system ignores the date field or returns HTTP 403
+
+#### Scenario: User modifies system-level anniversary remind_days
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new remind_days for a system-level anniversary
+- **THEN** the system updates remind_days and returns the updated record
+
+### Requirement: Anniversary supports three repeat types
+The system SHALL support NONE, YEARLY, and MONTHLY repeat types for anniversary records.
+
+#### Scenario: NONE type anniversary
+- **WHEN** an anniversary has `repeat_type=NONE`
+- **THEN** the "upcoming" calculation computes the date difference exactly once; if the date has passed, it is excluded from upcoming queries
+
+#### Scenario: YEARLY type anniversary
+- **WHEN** an anniversary has `repeat_type=YEARLY` and the original date is 2023-05-20
+- **THEN** the "upcoming" calculation finds the next occurrence in the current year; if that date has passed, it adds one year
+
+#### Scenario: YEARLY type with leap year February 29
+- **WHEN** an anniversary has `repeat_type=YEARLY` and the original date is 2020-02-29
+- **THEN** in a non-leap year, the system falls back to February 28 for the upcoming calculation
+
+#### Scenario: MONTHLY type anniversary
+- **WHEN** an anniversary has `repeat_type=MONTHLY` and the original date is 2023-05-20
+- **THEN** the "upcoming" calculation finds the next occurrence in the current month; if that date has passed, it adds one month
+
+### Requirement: Upcoming anniversaries query calculates remaining days
+The system SHALL expose `GET /api/v1/anniversaries/upcoming` that returns anniversaries sorted by nearest upcoming date with remaining days calculated.
+
+#### Scenario: User with multiple anniversaries requests upcoming list
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming
+- **THEN** the system returns anniversaries belonging to the user's couple, each with `remainingDays` calculated based on repeat type, sorted by `remainingDays` ascending
+
+#### Scenario: Upcoming query with limit parameter
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming?limit=3
+- **THEN** the system returns at most 3 anniversaries with the smallest remaining days
+
+#### Scenario: No upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming but all NONE-type anniversaries have passed
+- **THEN** the system returns an empty list
+
+### Requirement: Anniversary CRUD operations
+The system SHALL expose full CRUD operations for custom anniversaries.
+
+#### Scenario: Create anniversary with all fields
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with title, date, repeat_type, and remind_days
+- **THEN** the system validates the fields, creates the record associated with the user's couple, and returns HTTP 201 with the created anniversary
+
+#### Scenario: Create anniversary without remind_days
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries without remind_days
+- **THEN** the system creates the record with `remind_days=null` and returns HTTP 201
+
+#### Scenario: Update custom anniversary
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} for a custom anniversary with new title, date, repeat_type, or remind_days
+- **THEN** the system updates all provided fields and returns the updated record
+
+#### Scenario: Delete custom anniversary
+- **WHEN** an authenticated user sends DELETE /api/v1/anniversaries/{id} for a custom anniversary
+- **THEN** the system deletes the record and returns HTTP 204
+
+#### Scenario: List all anniversaries for couple
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries
+- **THEN** the system returns all anniversaries (both system and custom) belonging to the user's couple, ordered by date ascending
+
+### Requirement: Anniversary validation rules
+The system SHALL enforce validation rules on anniversary creation and updates.
+
+#### Scenario: Empty title rejected
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with an empty or blank title
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Future date accepted
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with a future date
+- **THEN** the system accepts the date and creates the record
+
+#### Scenario: Invalid repeat_type rejected
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with an invalid repeat_type value
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Unauthenticated request rejected
+- **WHEN** an unauthenticated user sends any anniversary API request
+- **THEN** the system returns HTTP 401
+
+#### Scenario: User without couple relationship rejected
+- **WHEN** an authenticated user who has not bound a couple sends GET /api/v1/anniversaries
+- **THEN** the system returns HTTP 403 with error message indicating no active couple relationship
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/specs/couple-start-date/spec.md b/openspec/changes/archive/2026-05-16-anniversary-module/specs/couple-start-date/spec.md
new file mode 100644
index 0000000..bb5771d
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/specs/couple-start-date/spec.md
@@ -0,0 +1,64 @@
+## ADDED Requirements
+
+### Requirement: Couple start date can be set after binding
+The system SHALL expose `PUT /api/v1/couple/start-date` that allows either partner to set or update the couple's start date.
+
+#### Scenario: User sets start date after binding
+- **WHEN** an authenticated user who has just bound a couple sends PUT /api/v1/couple/start-date with a valid date string
+- **THEN** the system updates `couple_relationship.created_at` to the specified date at midnight UTC+8 and returns the updated couple record
+
+#### Scenario: User updates start date later
+- **WHEN** an authenticated user in an existing couple sends PUT /api/v1/couple/start-date with a new date
+- **THEN** the system updates `couple_relationship.created_at` and cascades the update to the system-level anniversary's date field
+
+#### Scenario: Invalid date format rejected
+- **WHEN** an authenticated user sends PUT /api/v1/couple/start-date with an invalid date format
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Future start date rejected
+- **WHEN** an authenticated user sends PUT /api/v1/couple/start-date with a date in the future
+- **THEN** the system returns HTTP 400 with error message indicating start date cannot be in the future
+
+### Requirement: Binding flow includes start date setup prompt
+The Android app SHALL prompt the user to set the couple start date immediately after successful binding, with the option to skip.
+
+#### Scenario: User sets date during binding flow
+- **WHEN** a user completes the couple binding process
+- **THEN** the app displays a date picker BottomSheet with today's date as default
+- **AND WHEN** the user selects a date and confirms
+- **THEN** the app calls PUT /api/v1/couple/start-date and navigates to the home screen
+
+#### Scenario: User skips date setup during binding flow
+- **WHEN** a user completes the couple binding process
+- **THEN** the app displays a date picker BottomSheet
+- **AND WHEN** the user taps "Skip" or "Use default"
+- **THEN** the app uses the binding time as the default start date and navigates to the home screen without calling the API
+
+#### Scenario: User navigates back from date picker
+- **WHEN** a user completes the couple binding process and the date picker is shown
+- **AND WHEN** the user presses the system back button
+- **THEN** the app treats this as "skip" and navigates to the home screen with the default date
+
+### Requirement: Start date can be modified from profile page
+The Android app SHALL provide an entry point to modify the couple start date from the profile/settings page.
+
+#### Scenario: User modifies start date from profile
+- **WHEN** a user navigates to the profile page and taps "恋爱开始日期"
+- **THEN** the app displays a date picker with the current start date
+- **AND WHEN** the user selects a new date and confirms
+- **THEN** the app calls PUT /api/v1/couple/start-date and refreshes the home screen statistics
+
+#### Scenario: Start date change reflects immediately on home screen
+- **WHEN** a user successfully updates the couple start date
+- **THEN** the app updates the "在一起天数" statistic immediately without requiring app restart
+
+### Requirement: Start date affects home stats calculation
+The system SHALL use the couple start date as the authoritative source for "days together" calculation.
+
+#### Scenario: Days together calculated from start date
+- **WHEN** the home stats endpoint is called for a user with an active couple
+- **THEN** the system calculates `daysTogether` as the number of days between `couple_relationship.created_at` and the current date
+
+#### Scenario: Start date change updates days together
+- **WHEN** a couple's start date is updated via PUT /api/v1/couple/start-date
+- **THEN** subsequent calls to GET /api/v1/home/stats reflect the new days together count
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/specs/home-stats-api/spec.md b/openspec/changes/archive/2026-05-16-anniversary-module/specs/home-stats-api/spec.md
new file mode 100644
index 0000000..4a2b4dd
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/specs/home-stats-api/spec.md
@@ -0,0 +1,77 @@
+## ADDED Requirements
+
+### Requirement: Home stats uses real anniversary data for upcoming section
+The system SHALL query the Anniversary domain for real upcoming anniversary data instead of returning statically constructed mock data.
+
+#### Scenario: Home stats returns real upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/home/stats
+- **THEN** the system queries the Anniversary service for upcoming anniversaries belonging to the user's couple
+- **AND** the response includes the real anniversary titles and remaining days
+
+#### Scenario: Home stats with no upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/home/stats but there are no upcoming anniversaries
+- **THEN** the response includes an empty list for upcoming anniversaries
+
+## MODIFIED Requirements
+
+### Requirement: Home stats API returns aggregated data
+The system SHALL expose `GET /api/v1/home/stats` that returns aggregated home page data for the authenticated user.
+
+#### Scenario: Authenticated user requests home stats
+- **WHEN** an authenticated user sends GET /api/v1/home/stats
+- **THEN** the system returns HTTP 200 with a response containing stats cards, upcoming anniversaries, and recent memories
+
+### Requirement: Stats cards include five metrics
+The response SHALL include exactly five statistics: days together, memory count, location count, message count, and achievement count.
+
+#### Scenario: Days together calculation
+- **WHEN** the user has an active couple relationship
+- **THEN** the system calculates days together from `couple_relationship.created_at` (the user-configurable start date) to current date
+
+#### Scenario: Memory count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of memory records for the couple
+
+#### Scenario: Location count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the count of distinct locations across all memory records for the couple
+
+#### Scenario: Message count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of chat messages exchanged between the couple
+
+#### Scenario: Achievement count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of unlocked achievements for the couple
+
+### Requirement: Upcoming anniversary section
+The response SHALL include a list of upcoming anniversaries sorted by nearest date.
+
+#### Scenario: Anniversary within 30 days
+- **WHEN** there is an anniversary occurring within 30 days
+- **THEN** the response includes the anniversary title and remaining days calculated by the Anniversary domain service
+
+#### Scenario: No upcoming anniversary
+- **WHEN** there are no anniversaries within the upcoming window
+- **THEN** the response includes an empty list for upcoming anniversaries
+
+### Requirement: Recent memories timeline
+The response SHALL include recent memory records in reverse chronological order.
+
+#### Scenario: Recent memories with pagination
+- **WHEN** the user requests home stats
+- **THEN** the response includes the most recent 5 memory records with title, description snippet, date, and mood
+
+#### Scenario: Empty memory timeline
+- **WHEN** the couple has no memory records
+- **THEN** the response includes an empty list for recent memories
+
+## REMOVED Requirements
+
+### Requirement: Service layer uses mock data
+**Reason**: Replaced by real data queries from Anniversary domain and Couple repository.
+**Migration**: The `HomeAppServiceImpl` implementation has been updated to call `AnniversaryAppService` for upcoming anniversaries and `CoupleRepository` for the start date. No client migration needed.
+
+#### Scenario: Mock data consistency
+- **WHEN** the home stats endpoint is called
+- **THEN** the response structure and data types SHALL match the production schema exactly, with data values sourced from real database queries
diff --git a/openspec/changes/archive/2026-05-16-anniversary-module/tasks.md b/openspec/changes/archive/2026-05-16-anniversary-module/tasks.md
new file mode 100644
index 0000000..4ed41b2
--- /dev/null
+++ b/openspec/changes/archive/2026-05-16-anniversary-module/tasks.md
@@ -0,0 +1,127 @@
+## 1. Database Migration
+
+- [x] 1.1 Create Flyway V2 migration script: `anniversary` table with columns (id, couple_id, title, anniversary_date, repeat_type, remind_days, is_system, created_by, created_at)
+- [x] 1.2 Add indexes: `idx_anniversary_couple` on (couple_id), `idx_anniversary_date` on (anniversary_date)
+- [x] 1.3 Create data migration script to backfill system-level anniversaries for existing couple_relationship records
+- [x] 1.4 Verify migration runs successfully in local Docker environment
+
+## 2. Backend - Anniversary Domain Layer
+
+- [x] 2.1 Create `RepeatType` enum (NONE, YEARLY, MONTHLY)
+- [x] 2.2 Create `Anniversary` domain entity with business rules (title non-empty validation)
+- [x] 2.3 Create `AnniversaryRepository` interface with methods: save, findById, findByCoupleId, findByCoupleIdOrderByDate, deleteById, updateSystemAnniversaryDate
+- [x] 2.4 Create `AnniversaryDomainException` for domain-level validation failures
+
+## 3. Backend - Anniversary Infrastructure Layer
+
+- [x] 3.1 Create `AnniversaryDO` data object with MyBatis-Plus annotations
+- [x] 3.2 Create `AnniversaryMapper` extending BaseMapper
+- [x] 3.3 Create `AnniversaryRepositoryConverter` for Entity ↔ DO conversion
+- [x] 3.4 Create `AnniversaryRepositoryImpl` implementing repository interface
+
+## 4. Backend - Anniversary Application Layer
+
+- [x] 4.1 Create `AnniversaryCommands` record for create/update operations
+- [x] 4.2 Create `AnniversaryResult` record for query results (including `remainingDays`)
+- [x] 4.3 Create `AnniversaryAppService` interface
+- [x] 4.4 Implement `AnniversaryAppServiceImpl` with CRUD operations
+- [x] 4.5 Implement `findUpcoming(coupleId, limit)` with repeat type calculation algorithm (NONE/YEARLY/MONTHLY, leap year fallback)
+- [x] 4.6 Implement permission checks: verify anniversary belongs to user's couple
+
+## 5. Backend - Anniversary API Layer
+
+- [x] 5.1 Create `AnniversaryRequestDTO` (create/update)
+- [x] 5.2 Create `AnniversaryResponseDTO` (with remainingDays for upcoming query)
+- [x] 5.3 Create `AnniversaryRequestConverter`
+- [x] 5.4 Create `AnniversaryResponseConverter`
+- [x] 5.5 Create `AnniversaryController` with endpoints: GET /api/v1/anniversaries, POST /api/v1/anniversaries, PUT /api/v1/anniversaries/{id}, DELETE /api/v1/anniversaries/{id}, GET /api/v1/anniversaries/upcoming
+- [x] 5.6 Add `@PreAuthorize` or couple relationship validation to all endpoints
+
+## 6. Backend - Couple Start Date API
+
+- [x] 6.1 Create `UpdateStartDateRequestDTO` with date field
+- [x] 6.2 Add `updateStartDate(Long coupleId, LocalDate startDate)` to `CoupleAppService`
+- [x] 6.3 Implement start date update with cascade to system-level anniversary
+- [x] 6.4 Add `PUT /api/v1/couple/start-date` endpoint to `CoupleController`
+- [x] 6.5 Add validation: date not in future, valid format
+
+## 7. Backend - Modify Couple Binding Flow
+
+- [x] 7.1 Update `CoupleAppServiceImpl.bind()` to automatically create system-level anniversary after successful binding
+- [x] 7.2 Ensure creation happens within the same transaction as couple creation
+- [x] 7.3 Set default title to "恋爱开始日", repeat_type to YEARLY, is_system to true
+
+## 8. Backend - Update Home Stats
+
+- [x] 8.1 Add `AnniversaryAppService` dependency to `HomeAppServiceImpl`
+- [x] 8.2 Replace mock `upcomingAnniversaries` with real query to `AnniversaryAppService.findUpcoming()`
+- [x] 8.3 Update `daysTogether` calculation to use `Couple.createdAt` (already uses it, verify behavior)
+- [x] 8.4 Keep `recentMemories` as empty list or minimal mock until memory module is implemented
+- [x] 8.5 Verify `HomeStatsResult` and converter still match response schema
+
+## 9. Android - Anniversary Data Layer
+
+- [x] 9.1 Create `AnniversaryApi` Retrofit interface with all endpoints
+- [x] 9.2 Create `AnniversaryDto`, `CreateAnniversaryRequestDto`, `UpdateAnniversaryRequestDto`
+- [x] 9.3 Create `Anniversary` domain model (with RepeatType enum)
+- [x] 9.4 Create `AnniversaryRepository` interface
+- [x] 9.5 Create `AnniversaryRepositoryImpl`
+- [x] 9.6 Create `AnniversaryModule` for Hilt DI bindings
+
+## 10. Android - Anniversary Domain Layer
+
+- [x] 10.1 Create `GetAnniversariesUseCase`
+- [x] 10.2 Create `CreateAnniversaryUseCase`
+- [x] 10.3 Create `UpdateAnniversaryUseCase`
+- [x] 10.4 Create `DeleteAnniversaryUseCase`
+- [x] 10.5 Create `GetUpcomingAnniversariesUseCase`
+- [x] 10.6 Create `UpdateCoupleStartDateUseCase`
+
+## 11. Android - Anniversary List UI
+
+- [x] 11.1 Create `AnniversaryListScreen` and `AnniversaryListContent`
+- [x] 11.2 Create `AnniversaryListViewModel` with `AnniversaryListUiState` (Loading/Success/Error/Empty)
+- [x] 11.3 Create `AnniversaryListUiEvent` sealed class
+- [x] 11.4 Implement list UI: items sorted by date, system-level marked with special icon/color
+- [x] 11.5 Add floating action button to navigate to create page
+- [x] 11.6 Handle loading, empty, and error states
+
+## 12. Android - Anniversary Create/Edit UI
+
+- [x] 12.1 Create `AnniversaryEditScreen` and `AnniversaryEditContent` (reused for create and edit)
+- [x] 12.2 Create `AnniversaryEditViewModel` with form state management
+- [x] 12.3 Implement date picker using Android DatePickerDialog
+- [x] 12.4 Implement repeat type selector (NONE/YEARLY/MONTHLY)
+- [x] 12.5 Implement remind days input (optional, nullable)
+- [x] 12.6 Add form validation (title non-empty)
+- [x] 12.7 Handle create vs edit mode (pre-fill data for edit)
+
+## 13. Android - Binding Flow Enhancement
+
+- [x] 13.1 Create `StartDateBottomSheet` composable with date picker
+- [x] 13.2 Update `BindViewModel` to show BottomSheet after bind success
+- [x] 13.3 Update navigation graph: after BindScreen, show StartDateBottomSheet then navigate to Home
+- [x] 13.4 Implement skip behavior: do not call API, navigate to Home
+- [x] 13.5 Implement confirm behavior: call PUT /api/v1/couple/start-date, then navigate to Home
+
+## 14. Android - Home Screen Integration
+
+- [x] 14.1 Update `HomeViewModel` to call `GetUpcomingAnniversariesUseCase`
+- [x] 14.2 Update Home UI to display real upcoming anniversaries from API
+- [x] 14.3 Update Home UI "查看全部" to navigate to anniversary list
+- [x] 14.4 Update "在一起天数" to use real calculation (already connected, verify)
+
+## 15. Android - Profile Page Enhancement
+
+- [x] 15.1 Add "恋爱开始日期" entry to profile/settings page
+- [x] 15.2 Implement date picker dialog on tap
+- [x] 15.3 Call `UpdateCoupleStartDateUseCase` on confirm
+- [x] 15.4 Show success toast and refresh home stats
+
+## 16. Testing and Verification
+
+- [x] 16.1 Run backend unit tests for `AnniversaryAppServiceImpl` (upcoming calculation, repeat types)
+- [x] 16.2 Run backend integration tests for all new API endpoints
+- [x] 16.3 Test binding flow end-to-end: register → login → bind → set date → view home → view anniversary list
+- [x] 16.4 Test edge cases: leap year Feb 29, skip date setup, modify start date later, delete custom anniversary
+- [x] 16.5 Verify database migration works on existing data (couples without system-level anniversaries)
diff --git a/openspec/specs/anniversary-management/spec.md b/openspec/specs/anniversary-management/spec.md
new file mode 100644
index 0000000..c135b1c
--- /dev/null
+++ b/openspec/specs/anniversary-management/spec.md
@@ -0,0 +1,115 @@
+# anniversary-management Specification
+
+## Purpose
+TBD - created by archiving change anniversary-module. Update Purpose after archive.
+## Requirements
+### Requirement: Anniversary entity supports system and custom types
+The system SHALL store anniversaries with a flag distinguishing system-level records from user-created records.
+
+#### Scenario: System-level anniversary created on couple binding
+- **WHEN** two users successfully bind as a couple
+- **THEN** the system automatically creates an anniversary record with `is_system=true`, `title="恋爱开始日"`, `repeat_type=YEARLY`, and `date` equal to the couple's start date
+
+#### Scenario: Custom anniversary created by user
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with title, date, repeat_type, and optional remind_days
+- **THEN** the system creates an anniversary record with `is_system=false` and returns the created record
+
+### Requirement: System-level anniversary has restricted mutation rules
+The system SHALL enforce different mutation permissions for system-level and custom anniversaries.
+
+#### Scenario: User attempts to delete system-level anniversary
+- **WHEN** an authenticated user sends DELETE /api/v1/anniversaries/{id} for a system-level anniversary
+- **THEN** the system returns HTTP 403 with error code FORBIDDEN
+
+#### Scenario: User modifies system-level anniversary title
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new title for a system-level anniversary
+- **THEN** the system updates the title and returns the updated record
+
+#### Scenario: User attempts to modify system-level anniversary date directly
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new date for a system-level anniversary
+- **THEN** the system ignores the date field or returns HTTP 403
+
+#### Scenario: User modifies system-level anniversary remind_days
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} with a new remind_days for a system-level anniversary
+- **THEN** the system updates remind_days and returns the updated record
+
+### Requirement: Anniversary supports three repeat types
+The system SHALL support NONE, YEARLY, and MONTHLY repeat types for anniversary records.
+
+#### Scenario: NONE type anniversary
+- **WHEN** an anniversary has `repeat_type=NONE`
+- **THEN** the "upcoming" calculation computes the date difference exactly once; if the date has passed, it is excluded from upcoming queries
+
+#### Scenario: YEARLY type anniversary
+- **WHEN** an anniversary has `repeat_type=YEARLY` and the original date is 2023-05-20
+- **THEN** the "upcoming" calculation finds the next occurrence in the current year; if that date has passed, it adds one year
+
+#### Scenario: YEARLY type with leap year February 29
+- **WHEN** an anniversary has `repeat_type=YEARLY` and the original date is 2020-02-29
+- **THEN** in a non-leap year, the system falls back to February 28 for the upcoming calculation
+
+#### Scenario: MONTHLY type anniversary
+- **WHEN** an anniversary has `repeat_type=MONTHLY` and the original date is 2023-05-20
+- **THEN** the "upcoming" calculation finds the next occurrence in the current month; if that date has passed, it adds one month
+
+### Requirement: Upcoming anniversaries query calculates remaining days
+The system SHALL expose `GET /api/v1/anniversaries/upcoming` that returns anniversaries sorted by nearest upcoming date with remaining days calculated.
+
+#### Scenario: User with multiple anniversaries requests upcoming list
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming
+- **THEN** the system returns anniversaries belonging to the user's couple, each with `remainingDays` calculated based on repeat type, sorted by `remainingDays` ascending
+
+#### Scenario: Upcoming query with limit parameter
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming?limit=3
+- **THEN** the system returns at most 3 anniversaries with the smallest remaining days
+
+#### Scenario: No upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries/upcoming but all NONE-type anniversaries have passed
+- **THEN** the system returns an empty list
+
+### Requirement: Anniversary CRUD operations
+The system SHALL expose full CRUD operations for custom anniversaries.
+
+#### Scenario: Create anniversary with all fields
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with title, date, repeat_type, and remind_days
+- **THEN** the system validates the fields, creates the record associated with the user's couple, and returns HTTP 201 with the created anniversary
+
+#### Scenario: Create anniversary without remind_days
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries without remind_days
+- **THEN** the system creates the record with `remind_days=null` and returns HTTP 201
+
+#### Scenario: Update custom anniversary
+- **WHEN** an authenticated user sends PUT /api/v1/anniversaries/{id} for a custom anniversary with new title, date, repeat_type, or remind_days
+- **THEN** the system updates all provided fields and returns the updated record
+
+#### Scenario: Delete custom anniversary
+- **WHEN** an authenticated user sends DELETE /api/v1/anniversaries/{id} for a custom anniversary
+- **THEN** the system deletes the record and returns HTTP 204
+
+#### Scenario: List all anniversaries for couple
+- **WHEN** an authenticated user sends GET /api/v1/anniversaries
+- **THEN** the system returns all anniversaries (both system and custom) belonging to the user's couple, ordered by date ascending
+
+### Requirement: Anniversary validation rules
+The system SHALL enforce validation rules on anniversary creation and updates.
+
+#### Scenario: Empty title rejected
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with an empty or blank title
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Future date accepted
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with a future date
+- **THEN** the system accepts the date and creates the record
+
+#### Scenario: Invalid repeat_type rejected
+- **WHEN** an authenticated user sends POST /api/v1/anniversaries with an invalid repeat_type value
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Unauthenticated request rejected
+- **WHEN** an unauthenticated user sends any anniversary API request
+- **THEN** the system returns HTTP 401
+
+#### Scenario: User without couple relationship rejected
+- **WHEN** an authenticated user who has not bound a couple sends GET /api/v1/anniversaries
+- **THEN** the system returns HTTP 403 with error message indicating no active couple relationship
+
diff --git a/openspec/specs/couple-start-date/spec.md b/openspec/specs/couple-start-date/spec.md
new file mode 100644
index 0000000..7afd242
--- /dev/null
+++ b/openspec/specs/couple-start-date/spec.md
@@ -0,0 +1,68 @@
+# couple-start-date Specification
+
+## Purpose
+TBD - created by archiving change anniversary-module. Update Purpose after archive.
+## Requirements
+### Requirement: Couple start date can be set after binding
+The system SHALL expose `PUT /api/v1/couple/start-date` that allows either partner to set or update the couple's start date.
+
+#### Scenario: User sets start date after binding
+- **WHEN** an authenticated user who has just bound a couple sends PUT /api/v1/couple/start-date with a valid date string
+- **THEN** the system updates `couple_relationship.created_at` to the specified date at midnight UTC+8 and returns the updated couple record
+
+#### Scenario: User updates start date later
+- **WHEN** an authenticated user in an existing couple sends PUT /api/v1/couple/start-date with a new date
+- **THEN** the system updates `couple_relationship.created_at` and cascades the update to the system-level anniversary's date field
+
+#### Scenario: Invalid date format rejected
+- **WHEN** an authenticated user sends PUT /api/v1/couple/start-date with an invalid date format
+- **THEN** the system returns HTTP 400 with error code BAD_REQUEST
+
+#### Scenario: Future start date rejected
+- **WHEN** an authenticated user sends PUT /api/v1/couple/start-date with a date in the future
+- **THEN** the system returns HTTP 400 with error message indicating start date cannot be in the future
+
+### Requirement: Binding flow includes start date setup prompt
+The Android app SHALL prompt the user to set the couple start date immediately after successful binding, with the option to skip.
+
+#### Scenario: User sets date during binding flow
+- **WHEN** a user completes the couple binding process
+- **THEN** the app displays a date picker BottomSheet with today's date as default
+- **AND WHEN** the user selects a date and confirms
+- **THEN** the app calls PUT /api/v1/couple/start-date and navigates to the home screen
+
+#### Scenario: User skips date setup during binding flow
+- **WHEN** a user completes the couple binding process
+- **THEN** the app displays a date picker BottomSheet
+- **AND WHEN** the user taps "Skip" or "Use default"
+- **THEN** the app uses the binding time as the default start date and navigates to the home screen without calling the API
+
+#### Scenario: User navigates back from date picker
+- **WHEN** a user completes the couple binding process and the date picker is shown
+- **AND WHEN** the user presses the system back button
+- **THEN** the app treats this as "skip" and navigates to the home screen with the default date
+
+### Requirement: Start date can be modified from profile page
+The Android app SHALL provide an entry point to modify the couple start date from the profile/settings page.
+
+#### Scenario: User modifies start date from profile
+- **WHEN** a user navigates to the profile page and taps "恋爱开始日期"
+- **THEN** the app displays a date picker with the current start date
+- **AND WHEN** the user selects a new date and confirms
+- **THEN** the app calls PUT /api/v1/couple/start-date and refreshes the home screen statistics
+
+#### Scenario: Start date change reflects immediately on home screen
+- **WHEN** a user successfully updates the couple start date
+- **THEN** the app updates the "在一起天数" statistic immediately without requiring app restart
+
+### Requirement: Start date affects home stats calculation
+The system SHALL use the couple start date as the authoritative source for "days together" calculation.
+
+#### Scenario: Days together calculated from start date
+- **WHEN** the home stats endpoint is called for a user with an active couple
+- **THEN** the system calculates `daysTogether` as the number of days between `couple_relationship.created_at` and the current date
+
+#### Scenario: Start date change updates days together
+- **WHEN** a couple's start date is updated via PUT /api/v1/couple/start-date
+- **THEN** subsequent calls to GET /api/v1/home/stats reflect the new days together count
+
diff --git a/openspec/specs/home-stats-api/spec.md b/openspec/specs/home-stats-api/spec.md
index c64798b..819d66a 100644
--- a/openspec/specs/home-stats-api/spec.md
+++ b/openspec/specs/home-stats-api/spec.md
@@ -15,7 +15,7 @@ The response SHALL include exactly five statistics: days together, memory count,
 
 #### Scenario: Days together calculation
 - **WHEN** the user has an active couple relationship
-- **THEN** the system calculates days together from couple_relationship.created_at to current date
+- **THEN** the system calculates days together from `couple_relationship.created_at` (the user-configurable start date) to current date
 
 #### Scenario: Memory count
 - **WHEN** the user requests home stats
@@ -38,7 +38,7 @@ The response SHALL include a list of upcoming anniversaries sorted by nearest da
 
 #### Scenario: Anniversary within 30 days
 - **WHEN** there is an anniversary occurring within 30 days
-- **THEN** the response includes the anniversary title and remaining days
+- **THEN** the response includes the anniversary title and remaining days calculated by the Anniversary domain service
 
 #### Scenario: No upcoming anniversary
 - **WHEN** there are no anniversaries within the upcoming window
@@ -55,10 +55,15 @@ The response SHALL include recent memory records in reverse chronological order.
 - **WHEN** the couple has no memory records
 - **THEN** the response includes an empty list for recent memories
 
-### Requirement: Service layer uses mock data
-The AppService implementation SHALL return statically constructed data that matches the response schema.
+### Requirement: Home stats uses real anniversary data for upcoming section
+The system SHALL query the Anniversary domain for real upcoming anniversary data instead of returning statically constructed mock data.
 
-#### Scenario: Mock data consistency
-- **WHEN** the home stats endpoint is called
-- **THEN** the response structure and data types SHALL match the production schema exactly, with only the data values being mock
+#### Scenario: Home stats returns real upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/home/stats
+- **THEN** the system queries the Anniversary service for upcoming anniversaries belonging to the user's couple
+- **AND** the response includes the real anniversary titles and remaining days
+
+#### Scenario: Home stats with no upcoming anniversaries
+- **WHEN** an authenticated user sends GET /api/v1/home/stats but there are no upcoming anniversaries
+- **THEN** the response includes an empty list for upcoming anniversaries
 
diff --git a/src/api/src/main/java/cn/iven/lianji/api/advice/UnifiedResponseAdvice.java b/src/api/src/main/java/cn/iven/lianji/api/advice/UnifiedResponseAdvice.java
index 73eb9e6..9c55a13 100644
--- a/src/api/src/main/java/cn/iven/lianji/api/advice/UnifiedResponseAdvice.java
+++ b/src/api/src/main/java/cn/iven/lianji/api/advice/UnifiedResponseAdvice.java
@@ -37,7 +37,7 @@ public class UnifiedResponseAdvice implements ResponseBodyAdvice<Object> {
         }
 
         ResponseMessage<Object> responseMessage = body == null
-                ? ResponseMessage.created()
+                ? ResponseMessage.success()
                 : ResponseMessage.success(body);
 
         // String 类型需手动序列化，避免类型转换异常
diff --git a/src/api/src/main/java/cn/iven/lianji/api/controller/v1/anniversary/AnniversaryController.java b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/anniversary/AnniversaryController.java
new file mode 100644
index 0000000..b82f66c
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/anniversary/AnniversaryController.java
@@ -0,0 +1,88 @@
+package cn.iven.lianji.api.controller.v1.anniversary;
+
+import cn.iven.lianji.api.converter.anniversary.AnniversaryRequestConverter;
+import cn.iven.lianji.api.converter.anniversary.AnniversaryResponseConverter;
+import cn.iven.lianji.api.dto.anniversary.AnniversaryRequestDTO;
+import cn.iven.lianji.api.dto.anniversary.AnniversaryResponseDTO;
+import cn.iven.lianji.application.AnniversaryResult;
+import cn.iven.lianji.application.command.AnniversaryCommands;
+import cn.iven.lianji.application.service.AnniversaryAppService;
+import lombok.RequiredArgsConstructor;
+import org.springframework.security.core.context.SecurityContextHolder;
+import org.springframework.web.bind.annotation.DeleteMapping;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.PathVariable;
+import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.PutMapping;
+import org.springframework.web.bind.annotation.RequestBody;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
+import org.springframework.web.bind.annotation.RestController;
+
+import java.util.List;
+
+/**
+ * 纪念日接口（V1）。
+ * <p>提供纪念日 CRUD 及即将到来的纪念日查询能力。</p>
+ */
+@RestController
+@RequestMapping("/api/v1/anniversaries")
+@RequiredArgsConstructor
+public class AnniversaryController {
+
+    private final AnniversaryAppService anniversaryAppService;
+    private final AnniversaryRequestConverter requestConverter;
+    private final AnniversaryResponseConverter responseConverter;
+
+    @GetMapping
+    public List<AnniversaryResponseDTO> list() {
+        Long userId = getCurrentUserId();
+        List<AnniversaryResult> results = anniversaryAppService.findByCouple(userId);
+        return responseConverter.toDTOList(results);
+    }
+
+    @PostMapping
+    public AnniversaryResponseDTO create(@RequestBody AnniversaryRequestDTO request) {
+        Long userId = getCurrentUserId();
+        AnniversaryCommands.CreateCommand command = requestConverter.toCreateCommand(request);
+        AnniversaryResult result = anniversaryAppService.create(userId, command);
+        return responseConverter.toDTO(result);
+    }
+
+    @PutMapping("/{id}")
+    public AnniversaryResponseDTO update(@PathVariable Long id, @RequestBody AnniversaryRequestDTO request) {
+        Long userId = getCurrentUserId();
+        AnniversaryCommands.UpdateCommand command = requestConverter.toUpdateCommand(id, request);
+        AnniversaryResult result = anniversaryAppService.update(userId, command);
+        return responseConverter.toDTO(result);
+    }
+
+    @DeleteMapping("/{id}")
+    public void delete(@PathVariable Long id) {
+        Long userId = getCurrentUserId();
+        anniversaryAppService.delete(userId, id);
+    }
+
+    @GetMapping("/{id}")
+    public AnniversaryResponseDTO getById(@PathVariable Long id) {
+        Long userId = getCurrentUserId();
+        AnniversaryResult result = anniversaryAppService.findById(userId, id);
+        return responseConverter.toDTO(result);
+    }
+
+    @GetMapping("/upcoming")
+    public List<AnniversaryResponseDTO> upcoming(@RequestParam(defaultValue = "5") Integer limit) {
+        Long userId = getCurrentUserId();
+        List<AnniversaryResult> results = anniversaryAppService.findUpcoming(userId, limit);
+        return responseConverter.toDTOList(results);
+    }
+
+    /**
+     * 从 SecurityContext 获取当前登录用户 ID。
+     * <p>JWT 过滤器将 userId 写入 username 字段。</p>
+     */
+    private Long getCurrentUserId() {
+        String username = SecurityContextHolder.getContext().getAuthentication().getName();
+        return Long.valueOf(username);
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/controller/v1/couple/CoupleController.java b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/couple/CoupleController.java
index 52d4c4f..f8265f1 100644
--- a/src/api/src/main/java/cn/iven/lianji/api/controller/v1/couple/CoupleController.java
+++ b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/couple/CoupleController.java
@@ -4,12 +4,14 @@ import cn.iven.lianji.api.converter.couple.CoupleResponseConverter;
 import cn.iven.lianji.api.dto.couple.BindCoupleRequestDTO;
 import cn.iven.lianji.api.dto.couple.BindingCodeResponseDTO;
 import cn.iven.lianji.api.dto.couple.CoupleResponseDTO;
+import cn.iven.lianji.api.dto.couple.UpdateStartDateRequestDTO;
 import cn.iven.lianji.application.CoupleResult;
 import cn.iven.lianji.application.service.CoupleAppService;
 import lombok.RequiredArgsConstructor;
 import org.springframework.security.core.context.SecurityContextHolder;
 import org.springframework.web.bind.annotation.GetMapping;
 import org.springframework.web.bind.annotation.PostMapping;
+import org.springframework.web.bind.annotation.PutMapping;
 import org.springframework.web.bind.annotation.RequestBody;
 import org.springframework.web.bind.annotation.RequestMapping;
 import org.springframework.web.bind.annotation.RestController;
@@ -47,6 +49,13 @@ public class CoupleController {
         return responseConverter.toDTO(result);
     }
 
+    @PutMapping("/start-date")
+    public CoupleResponseDTO updateStartDate(@RequestBody UpdateStartDateRequestDTO request) {
+        Long userId = getCurrentUserId();
+        CoupleResult result = coupleAppService.updateStartDate(userId, request.getStartDate());
+        return responseConverter.toDTO(result);
+    }
+
     /**
      * 从 SecurityContext 获取当前登录用户 ID。
      * <p>JWT 过滤器将 userId 写入 username 字段。</p>
diff --git a/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryRequestConverter.java b/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryRequestConverter.java
new file mode 100644
index 0000000..38e64b4
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryRequestConverter.java
@@ -0,0 +1,38 @@
+package cn.iven.lianji.api.converter.anniversary;
+
+import cn.iven.lianji.api.dto.anniversary.AnniversaryRequestDTO;
+import cn.iven.lianji.application.command.AnniversaryCommands;
+import org.springframework.stereotype.Component;
+
+/**
+ * 纪念日请求转换器。
+ * <p>负责 {@code AnniversaryRequestDTO → AnniversaryCommands} 的入站转换。</p>
+ */
+@Component
+public class AnniversaryRequestConverter {
+
+    public AnniversaryCommands.CreateCommand toCreateCommand(AnniversaryRequestDTO dto) {
+        if (dto == null) {
+            return null;
+        }
+        return new AnniversaryCommands.CreateCommand(
+                dto.getTitle(),
+                dto.getDate(),
+                dto.getRepeatType(),
+                dto.getRemindDays()
+        );
+    }
+
+    public AnniversaryCommands.UpdateCommand toUpdateCommand(Long id, AnniversaryRequestDTO dto) {
+        if (dto == null) {
+            return null;
+        }
+        return new AnniversaryCommands.UpdateCommand(
+                id,
+                dto.getTitle(),
+                dto.getDate(),
+                dto.getRepeatType(),
+                dto.getRemindDays()
+        );
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryResponseConverter.java b/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryResponseConverter.java
new file mode 100644
index 0000000..2859f88
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/converter/anniversary/AnniversaryResponseConverter.java
@@ -0,0 +1,42 @@
+package cn.iven.lianji.api.converter.anniversary;
+
+import cn.iven.lianji.api.dto.anniversary.AnniversaryResponseDTO;
+import cn.iven.lianji.application.AnniversaryResult;
+import org.springframework.stereotype.Component;
+
+import java.util.List;
+
+/**
+ * 纪念日响应转换器。
+ * <p>负责 {@code AnniversaryResult → AnniversaryResponseDTO} 的出站转换。</p>
+ */
+@Component
+public class AnniversaryResponseConverter {
+
+    public AnniversaryResponseDTO toDTO(AnniversaryResult result) {
+        if (result == null) {
+            return null;
+        }
+        return AnniversaryResponseDTO.builder()
+                .id(result.id())
+                .coupleId(result.coupleId())
+                .title(result.title())
+                .date(result.date())
+                .repeatType(result.repeatType())
+                .remindDays(result.remindDays())
+                .isSystem(result.isSystem())
+                .createdBy(result.createdBy())
+                .createdAt(result.createdAt())
+                .remainingDays(result.remainingDays())
+                .build();
+    }
+
+    public List<AnniversaryResponseDTO> toDTOList(List<AnniversaryResult> results) {
+        if (results == null) {
+            return null;
+        }
+        return results.stream()
+                .map(this::toDTO)
+                .toList();
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryRequestDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryRequestDTO.java
new file mode 100644
index 0000000..c02eaf2
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryRequestDTO.java
@@ -0,0 +1,27 @@
+package cn.iven.lianji.api.dto.anniversary;
+
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+import lombok.Builder;
+import lombok.Data;
+
+import java.time.LocalDate;
+
+/**
+ * 纪念日请求 DTO（创建/更新）。
+ */
+@Data
+@Builder
+public class AnniversaryRequestDTO {
+
+    /** 纪念日标题 */
+    private String title;
+
+    /** 纪念日日期 */
+    private LocalDate date;
+
+    /** 重复类型 */
+    private RepeatType repeatType;
+
+    /** 提前提醒天数 */
+    private Integer remindDays;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryResponseDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryResponseDTO.java
new file mode 100644
index 0000000..eaf812b
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/anniversary/AnniversaryResponseDTO.java
@@ -0,0 +1,46 @@
+package cn.iven.lianji.api.dto.anniversary;
+
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+import lombok.Builder;
+import lombok.Data;
+
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+
+/**
+ * 纪念日响应 DTO。
+ */
+@Data
+@Builder
+public class AnniversaryResponseDTO {
+
+    /** 纪念日ID */
+    private Long id;
+
+    /** 情侣关系ID */
+    private Long coupleId;
+
+    /** 纪念日标题 */
+    private String title;
+
+    /** 纪念日日期 */
+    private LocalDate date;
+
+    /** 重复类型 */
+    private RepeatType repeatType;
+
+    /** 提前提醒天数 */
+    private Integer remindDays;
+
+    /** 是否为系统级纪念日 */
+    private Boolean isSystem;
+
+    /** 创建者用户ID */
+    private Long createdBy;
+
+    /** 创建时间 */
+    private OffsetDateTime createdAt;
+
+    /** 距离下一个纪念日的剩余天数（仅 upcoming 查询返回） */
+    private Integer remainingDays;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/couple/UpdateStartDateRequestDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/couple/UpdateStartDateRequestDTO.java
new file mode 100644
index 0000000..6247d77
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/couple/UpdateStartDateRequestDTO.java
@@ -0,0 +1,17 @@
+package cn.iven.lianji.api.dto.couple;
+
+import lombok.Builder;
+import lombok.Data;
+
+import java.time.LocalDate;
+
+/**
+ * 更新恋爱开始日期请求 DTO。
+ */
+@Data
+@Builder
+public class UpdateStartDateRequestDTO {
+
+    /** 新的恋爱开始日期 */
+    private LocalDate startDate;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/AnniversaryResult.java b/src/api/src/main/java/cn/iven/lianji/application/AnniversaryResult.java
new file mode 100644
index 0000000..3729c96
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/AnniversaryResult.java
@@ -0,0 +1,23 @@
+package cn.iven.lianji.application;
+
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+
+/**
+ * 纪念日应用层结果对象。
+ * <p>封装查询或操作后的纪念日数据，供 API 层转换为 {@code AnniversaryResponseDTO}。</p>
+ */
+public record AnniversaryResult(
+        Long id,
+        Long coupleId,
+        String title,
+        LocalDate date,
+        RepeatType repeatType,
+        Integer remindDays,
+        Boolean isSystem,
+        Long createdBy,
+        OffsetDateTime createdAt,
+        Integer remainingDays
+) {}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/command/AnniversaryCommands.java b/src/api/src/main/java/cn/iven/lianji/application/command/AnniversaryCommands.java
new file mode 100644
index 0000000..6237378
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/command/AnniversaryCommands.java
@@ -0,0 +1,34 @@
+package cn.iven.lianji.application.command;
+
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+
+import java.time.LocalDate;
+
+/**
+ * 纪念日相关命令对象。
+ */
+public class AnniversaryCommands {
+
+    private AnniversaryCommands() {}
+
+    /**
+     * 创建纪念日命令。
+     */
+    public record CreateCommand(
+            String title,
+            LocalDate date,
+            RepeatType repeatType,
+            Integer remindDays
+    ) {}
+
+    /**
+     * 更新纪念日命令。
+     */
+    public record UpdateCommand(
+            Long id,
+            String title,
+            LocalDate date,
+            RepeatType repeatType,
+            Integer remindDays
+    ) {}
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/AnniversaryAppService.java b/src/api/src/main/java/cn/iven/lianji/application/service/AnniversaryAppService.java
new file mode 100644
index 0000000..c98fb25
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/AnniversaryAppService.java
@@ -0,0 +1,65 @@
+package cn.iven.lianji.application.service;
+
+import cn.iven.lianji.application.AnniversaryResult;
+import cn.iven.lianji.application.command.AnniversaryCommands;
+
+import java.util.List;
+
+/**
+ * 纪念日应用服务接口。
+ * <p>编排纪念日 CRUD 及即将到来的纪念日查询用例。</p>
+ */
+public interface AnniversaryAppService {
+
+    /**
+     * 创建纪念日。
+     *
+     * @param userId  当前用户 ID
+     * @param command 创建命令
+     * @return 创建后的纪念日数据
+     */
+    AnniversaryResult create(Long userId, AnniversaryCommands.CreateCommand command);
+
+    /**
+     * 更新纪念日。
+     *
+     * @param userId  当前用户 ID
+     * @param command 更新命令
+     * @return 更新后的纪念日数据
+     */
+    AnniversaryResult update(Long userId, AnniversaryCommands.UpdateCommand command);
+
+    /**
+     * 删除纪念日。
+     *
+     * @param userId       当前用户 ID
+     * @param anniversaryId 纪念日 ID
+     */
+    void delete(Long userId, Long anniversaryId);
+
+    /**
+     * 查询当前用户情侣的所有纪念日。
+     *
+     * @param userId 当前用户 ID
+     * @return 纪念日列表
+     */
+    List<AnniversaryResult> findByCouple(Long userId);
+
+    /**
+     * 查询即将到来的纪念日（按剩余天数排序）。
+     *
+     * @param userId 当前用户 ID
+     * @param limit  最大返回条数
+     * @return 即将到来的纪念日列表
+     */
+    List<AnniversaryResult> findUpcoming(Long userId, Integer limit);
+
+    /**
+     * 根据 ID 查询单个纪念日。
+     *
+     * @param userId        当前用户 ID
+     * @param anniversaryId 纪念日 ID
+     * @return 纪念日数据
+     */
+    AnniversaryResult findById(Long userId, Long anniversaryId);
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/CoupleAppService.java b/src/api/src/main/java/cn/iven/lianji/application/service/CoupleAppService.java
index 1ea5599..aa8c33e 100644
--- a/src/api/src/main/java/cn/iven/lianji/application/service/CoupleAppService.java
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/CoupleAppService.java
@@ -2,9 +2,11 @@ package cn.iven.lianji.application.service;
 
 import cn.iven.lianji.application.CoupleResult;
 
+import java.time.LocalDate;
+
 /**
  * 情侣关系应用服务接口。
- * <p>编排绑定码生成、关系绑定及状态查询用例。</p>
+ * <p>编排绑定码生成、关系绑定、状态查询及开始日期更新用例。</p>
  */
 public interface CoupleAppService {
 
@@ -32,4 +34,13 @@ public interface CoupleAppService {
      * @return 关系数据，若未绑定则返回 null
      */
     CoupleResult getRelationship(Long userId);
+
+    /**
+     * 更新恋爱开始日期，并级联更新系统级纪念日。
+     *
+     * @param userId    当前用户 ID
+     * @param startDate 新的恋爱开始日期
+     * @return 更新后的关系数据
+     */
+    CoupleResult updateStartDate(Long userId, LocalDate startDate);
 }
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/impl/AnniversaryAppServiceImpl.java b/src/api/src/main/java/cn/iven/lianji/application/service/impl/AnniversaryAppServiceImpl.java
new file mode 100644
index 0000000..57d0c33
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/impl/AnniversaryAppServiceImpl.java
@@ -0,0 +1,214 @@
+package cn.iven.lianji.application.service.impl;
+
+import cn.iven.lianji.application.AnniversaryResult;
+import cn.iven.lianji.application.command.AnniversaryCommands;
+import cn.iven.lianji.application.service.AnniversaryAppService;
+import cn.iven.lianji.domain.exception.ErrorCode;
+import cn.iven.lianji.domain.exception.ForbiddenException;
+import cn.iven.lianji.domain.exception.NotFoundException;
+import cn.iven.lianji.domain.model.entity.Anniversary;
+import cn.iven.lianji.domain.model.entity.Couple;
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+import cn.iven.lianji.domain.repository.AnniversaryRepository;
+import cn.iven.lianji.domain.repository.CoupleRepository;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Service;
+import org.springframework.transaction.annotation.Transactional;
+
+import java.time.LocalDate;
+import java.time.temporal.ChronoUnit;
+import java.util.Comparator;
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 纪念日应用服务实现。
+ * <p>编排纪念日 CRUD 及即将到来的纪念日计算逻辑。</p>
+ */
+@Service
+@RequiredArgsConstructor
+public class AnniversaryAppServiceImpl implements AnniversaryAppService {
+
+    private final AnniversaryRepository anniversaryRepository;
+    private final CoupleRepository coupleRepository;
+
+    @Override
+    @Transactional
+    public AnniversaryResult create(Long userId, AnniversaryCommands.CreateCommand command) {
+        Couple couple = getCoupleOrThrow(userId);
+        Anniversary anniversary = Anniversary.create(
+                couple.getId(),
+                command.title(),
+                command.date(),
+                command.repeatType(),
+                command.remindDays(),
+                userId
+        );
+        anniversary = anniversaryRepository.save(anniversary);
+        return toResult(anniversary, null);
+    }
+
+    @Override
+    @Transactional
+    public AnniversaryResult update(Long userId, AnniversaryCommands.UpdateCommand command) {
+        Couple couple = getCoupleOrThrow(userId);
+        Anniversary anniversary = anniversaryRepository.findById(command.id())
+                .orElseThrow(() -> new NotFoundException(ErrorCode.NotFound.NOT_FOUND));
+
+        verifyOwnership(couple, anniversary);
+        if (Boolean.TRUE.equals(anniversary.getIsSystem())) {
+            throw new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "系统级纪念日不可修改");
+        }
+
+        anniversary.update(command.title(), command.date(), command.repeatType(), command.remindDays());
+        anniversary = anniversaryRepository.save(anniversary);
+        return toResult(anniversary, null);
+    }
+
+    @Override
+    @Transactional
+    public void delete(Long userId, Long anniversaryId) {
+        Couple couple = getCoupleOrThrow(userId);
+        Anniversary anniversary = anniversaryRepository.findById(anniversaryId)
+                .orElseThrow(() -> new NotFoundException(ErrorCode.NotFound.NOT_FOUND));
+
+        verifyOwnership(couple, anniversary);
+        if (Boolean.TRUE.equals(anniversary.getIsSystem())) {
+            throw new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "系统级纪念日不可删除");
+        }
+
+        anniversaryRepository.deleteById(anniversaryId);
+    }
+
+    @Override
+    public List<AnniversaryResult> findByCouple(Long userId) {
+        Couple couple = getCoupleOrThrow(userId);
+        return anniversaryRepository.findByCoupleId(couple.getId()).stream()
+                .map(a -> toResult(a, null))
+                .toList();
+    }
+
+    @Override
+    public AnniversaryResult findById(Long userId, Long anniversaryId) {
+        Couple couple = getCoupleOrThrow(userId);
+        Anniversary anniversary = anniversaryRepository.findById(anniversaryId)
+                .orElseThrow(() -> new NotFoundException(ErrorCode.NotFound.NOT_FOUND));
+        verifyOwnership(couple, anniversary);
+        return toResult(anniversary, null);
+    }
+
+    @Override
+    public List<AnniversaryResult> findUpcoming(Long userId, Integer limit) {
+        Couple couple = getCoupleOrThrow(userId);
+        LocalDate today = LocalDate.now();
+
+        return anniversaryRepository.findByCoupleId(couple.getId()).stream()
+                .map(a -> {
+                    Integer remainingDays = calculateRemainingDays(a, today);
+                    return toResult(a, remainingDays);
+                })
+                .filter(r -> r.remainingDays() != null && r.remainingDays() >= 0)
+                .sorted(Comparator.comparingInt(AnniversaryResult::remainingDays))
+                .limit(limit != null && limit > 0 ? limit : 5)
+                .toList();
+    }
+
+    private Couple getCoupleOrThrow(Long userId) {
+        return coupleRepository.findByUserId(userId)
+                .orElseThrow(() -> new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "用户未绑定情侣关系"));
+    }
+
+    private void verifyOwnership(Couple couple, Anniversary anniversary) {
+        if (!couple.getId().equals(anniversary.getCoupleId())) {
+            throw new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "无权操作该纪念日");
+        }
+    }
+
+    /**
+     * 计算距离下一个纪念日的剩余天数。
+     *
+     * @param anniversary 纪念日实体
+     * @param today       今天日期
+     * @return 剩余天数，null 表示不重复且已过期
+     */
+    Integer calculateRemainingDays(Anniversary anniversary, LocalDate today) {
+        LocalDate baseDate = anniversary.getDate();
+        if (baseDate == null) {
+            return null;
+        }
+
+        RepeatType repeatType = anniversary.getRepeatType() != null
+                ? anniversary.getRepeatType() : RepeatType.NONE;
+
+        return switch (repeatType) {
+            case NONE -> {
+                long days = ChronoUnit.DAYS.between(today, baseDate);
+                yield days >= 0 ? (int) days : null;
+            }
+            case YEARLY -> {
+                LocalDate nextOccurrence = findNextYearlyOccurrence(baseDate, today);
+                yield (int) ChronoUnit.DAYS.between(today, nextOccurrence);
+            }
+            case MONTHLY -> {
+                LocalDate nextOccurrence = findNextMonthlyOccurrence(baseDate, today);
+                yield (int) ChronoUnit.DAYS.between(today, nextOccurrence);
+            }
+        };
+    }
+
+    private LocalDate findNextYearlyOccurrence(LocalDate baseDate, LocalDate today) {
+        LocalDate candidate = baseDate.withYear(today.getYear());
+
+        // Feb 29 fallback: non-leap year -> Feb 28
+        if (baseDate.getMonthValue() == 2 && baseDate.getDayOfMonth() == 29) {
+            if (!candidate.isLeapYear()) {
+                candidate = candidate.withDayOfMonth(28);
+            }
+        }
+
+        if (candidate.isBefore(today) || candidate.isEqual(today)) {
+            candidate = candidate.plusYears(1);
+            // Re-check leap year for next year
+            if (baseDate.getMonthValue() == 2 && baseDate.getDayOfMonth() == 29) {
+                if (!candidate.isLeapYear()) {
+                    candidate = candidate.withDayOfMonth(28);
+                } else {
+                    candidate = candidate.withDayOfMonth(29);
+                }
+            }
+        }
+
+        return candidate;
+    }
+
+    private LocalDate findNextMonthlyOccurrence(LocalDate baseDate, LocalDate today) {
+        LocalDate candidate = baseDate.withYear(today.getYear()).withMonth(today.getMonthValue());
+
+        // Handle day overflow (e.g., Jan 31 -> Feb 28/29)
+        int dayOfMonth = Math.min(baseDate.getDayOfMonth(), candidate.lengthOfMonth());
+        candidate = candidate.withDayOfMonth(dayOfMonth);
+
+        if (candidate.isBefore(today) || candidate.isEqual(today)) {
+            candidate = candidate.plusMonths(1);
+            dayOfMonth = Math.min(baseDate.getDayOfMonth(), candidate.lengthOfMonth());
+            candidate = candidate.withDayOfMonth(dayOfMonth);
+        }
+
+        return candidate;
+    }
+
+    private AnniversaryResult toResult(Anniversary anniversary, Integer remainingDays) {
+        return new AnniversaryResult(
+                anniversary.getId(),
+                anniversary.getCoupleId(),
+                anniversary.getTitle(),
+                anniversary.getDate(),
+                anniversary.getRepeatType(),
+                anniversary.getRemindDays(),
+                anniversary.getIsSystem(),
+                anniversary.getCreatedBy(),
+                anniversary.getCreatedAt(),
+                remainingDays
+        );
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImpl.java b/src/api/src/main/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImpl.java
index 1338340..2ace58c 100644
--- a/src/api/src/main/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImpl.java
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImpl.java
@@ -5,7 +5,10 @@ import cn.iven.lianji.application.service.CoupleAppService;
 import cn.iven.lianji.domain.exception.BadRequestException;
 import cn.iven.lianji.domain.exception.ConflictException;
 import cn.iven.lianji.domain.exception.ErrorCode;
+import cn.iven.lianji.domain.exception.ForbiddenException;
+import cn.iven.lianji.domain.model.entity.Anniversary;
 import cn.iven.lianji.domain.model.entity.Couple;
+import cn.iven.lianji.domain.repository.AnniversaryRepository;
 import cn.iven.lianji.domain.repository.CoupleRepository;
 import cn.iven.lianji.infrastructure.config.CoupleProperties;
 import lombok.RequiredArgsConstructor;
@@ -13,6 +16,9 @@ import org.springframework.data.redis.core.StringRedisTemplate;
 import org.springframework.stereotype.Service;
 import org.springframework.transaction.annotation.Transactional;
 
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+import java.time.ZoneOffset;
 import java.util.Random;
 import java.util.concurrent.TimeUnit;
 
@@ -25,6 +31,7 @@ import java.util.concurrent.TimeUnit;
 public class CoupleAppServiceImpl implements CoupleAppService {
 
     private final CoupleRepository coupleRepository;
+    private final AnniversaryRepository anniversaryRepository;
     private final StringRedisTemplate redisTemplate;
     private final CoupleProperties coupleProperties;
     private final Random random = new Random();
@@ -81,6 +88,14 @@ public class CoupleAppServiceImpl implements CoupleAppService {
         Couple couple = Couple.create(partnerId, userId);
         couple = coupleRepository.save(couple);
 
+        // 自动创建系统级纪念日（恋爱开始日）
+        Anniversary systemAnniversary = Anniversary.createSystem(
+                couple.getId(),
+                "恋爱开始日",
+                couple.getCreatedAt().toLocalDate()
+        );
+        anniversaryRepository.save(systemAnniversary);
+
         // 绑定成功后清除绑定码
         redisTemplate.delete(codeKey);
         redisTemplate.delete(userBindingKey(partnerId));
@@ -95,6 +110,29 @@ public class CoupleAppServiceImpl implements CoupleAppService {
                 .orElse(null);
     }
 
+    @Override
+    @Transactional
+    public CoupleResult updateStartDate(Long userId, LocalDate startDate) {
+        if (startDate == null) {
+            throw new BadRequestException(ErrorCode.BadRequest.BAD_REQUEST, "开始日期不能为空");
+        }
+        if (startDate.isAfter(LocalDate.now())) {
+            throw new BadRequestException(ErrorCode.BadRequest.BAD_REQUEST, "开始日期不能为未来日期");
+        }
+
+        Couple couple = coupleRepository.findByUserId(userId)
+                .orElseThrow(() -> new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "用户未绑定情侣关系"));
+
+        // 更新 couple_relationship.created_at
+        couple.setCreatedAt(startDate.atStartOfDay().atOffset(ZoneOffset.UTC));
+        couple = coupleRepository.save(couple);
+
+        // 级联更新系统级纪念日日期
+        anniversaryRepository.updateSystemAnniversaryDate(couple.getId(), startDate);
+
+        return toResult(couple);
+    }
+
     private boolean isInRelationship(Long userId) {
         return coupleRepository.findByUserId(userId).isPresent();
     }
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java b/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java
index 5b79fb8..90b3a97 100644
--- a/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java
@@ -1,6 +1,8 @@
 package cn.iven.lianji.application.service.impl;
 
+import cn.iven.lianji.application.AnniversaryResult;
 import cn.iven.lianji.application.HomeStatsResult;
+import cn.iven.lianji.application.service.AnniversaryAppService;
 import cn.iven.lianji.application.service.HomeAppService;
 import cn.iven.lianji.domain.exception.ErrorCode;
 import cn.iven.lianji.domain.exception.ForbiddenException;
@@ -11,6 +13,7 @@ import org.springframework.stereotype.Service;
 
 import java.time.LocalDate;
 import java.time.temporal.ChronoUnit;
+import java.util.Collections;
 import java.util.List;
 
 /**
@@ -21,6 +24,7 @@ import java.util.List;
 public class HomeAppServiceImpl implements HomeAppService {
 
     private final CoupleRepository coupleRepository;
+    private final AnniversaryAppService anniversaryAppService;
 
     @Override
     public HomeStatsResult getStats(Long userId) {
@@ -30,25 +34,19 @@ public class HomeAppServiceImpl implements HomeAppService {
         int daysTogether = (int) ChronoUnit.DAYS.between(
                 couple.getCreatedAt().toLocalDate(), LocalDate.now());
 
-        List<HomeStatsResult.AnniversaryCardResult> upcomingAnniversaries = List.of(
-                new HomeStatsResult.AnniversaryCardResult("一周年纪念日", 3)
-        );
+        List<HomeStatsResult.AnniversaryCardResult> upcomingAnniversaries =
+                anniversaryAppService.findUpcoming(userId, 3).stream()
+                        .map(r -> new HomeStatsResult.AnniversaryCardResult(r.title(), r.remainingDays()))
+                        .toList();
 
-        List<HomeStatsResult.MemoryTimelineItemResult> recentMemories = List.of(
-                new HomeStatsResult.MemoryTimelineItemResult(
-                        1L, "第一次约会", "今天和TA去了人民公园，天气很好...", "2026-05-18", 1),
-                new HomeStatsResult.MemoryTimelineItemResult(
-                        2L, "一起看电影", "看了《恋恋笔记本》，非常感动...", "2026-05-15", 2),
-                new HomeStatsResult.MemoryTimelineItemResult(
-                        3L, "一起做晚饭", "做了意大利面，虽然卖相不好但很好吃...", "2026-05-12", 3)
-        );
+        List<HomeStatsResult.MemoryTimelineItemResult> recentMemories = Collections.emptyList();
 
         return new HomeStatsResult(
                 daysTogether,
-                52,
-                18,
-                128,
-                12,
+                0,
+                0,
+                0,
+                0,
                 upcomingAnniversaries,
                 recentMemories
         );
diff --git a/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Anniversary.java b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Anniversary.java
new file mode 100644
index 0000000..b57cc44
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Anniversary.java
@@ -0,0 +1,77 @@
+package cn.iven.lianji.domain.model.entity;
+
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+import lombok.Builder;
+import lombok.Data;
+
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+
+/**
+ * 纪念日领域实体。
+ * <p>封装纪念日创建、更新等业务规则。</p>
+ */
+@Data
+@Builder
+public class Anniversary {
+
+    private Long id;
+    private Long coupleId;
+    private String title;
+    private LocalDate date;
+    private RepeatType repeatType;
+    private Integer remindDays;
+    private Boolean isSystem;
+    private Long createdBy;
+    private OffsetDateTime createdAt;
+
+    /**
+     * 工厂方法：创建用户自定义纪念日。
+     */
+    public static Anniversary create(Long coupleId, String title, LocalDate date,
+                                     RepeatType repeatType, Integer remindDays, Long createdBy) {
+        if (title == null || title.trim().isEmpty()) {
+            throw new IllegalArgumentException("纪念日标题不能为空");
+        }
+        return Anniversary.builder()
+                .coupleId(coupleId)
+                .title(title.trim())
+                .date(date)
+                .repeatType(repeatType != null ? repeatType : RepeatType.NONE)
+                .remindDays(remindDays)
+                .isSystem(false)
+                .createdBy(createdBy)
+                .build();
+    }
+
+    /**
+     * 工厂方法：创建系统级纪念日（恋爱开始日）。
+     */
+    public static Anniversary createSystem(Long coupleId, String title, LocalDate date) {
+        return Anniversary.builder()
+                .coupleId(coupleId)
+                .title(title)
+                .date(date)
+                .repeatType(RepeatType.YEARLY)
+                .isSystem(true)
+                .build();
+    }
+
+    /**
+     * 更新可编辑字段（仅用于自定义纪念日，系统级需通过专门的级联更新修改日期）。
+     */
+    public void update(String title, LocalDate date, RepeatType repeatType, Integer remindDays) {
+        if (title != null && !title.trim().isEmpty()) {
+            this.title = title.trim();
+        }
+        if (date != null) {
+            this.date = date;
+        }
+        if (repeatType != null) {
+            this.repeatType = repeatType;
+        }
+        if (remindDays != null) {
+            this.remindDays = remindDays;
+        }
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
index 2469e41..786d64a 100644
--- a/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
+++ b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
@@ -29,6 +29,7 @@ public class Couple {
         return Couple.builder()
                 .userAId(userAId)
                 .userBId(userBId)
+                .createdAt(OffsetDateTime.now())
                 .build();
     }
 }
diff --git a/src/api/src/main/java/cn/iven/lianji/domain/model/enumerate/RepeatType.java b/src/api/src/main/java/cn/iven/lianji/domain/model/enumerate/RepeatType.java
new file mode 100644
index 0000000..6451bd6
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/domain/model/enumerate/RepeatType.java
@@ -0,0 +1,10 @@
+package cn.iven.lianji.domain.model.enumerate;
+
+/**
+ * 纪念日重复类型枚举。
+ */
+public enum RepeatType {
+    NONE,    // 不重复
+    YEARLY,  // 每年重复
+    MONTHLY  // 每月重复
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/domain/repository/AnniversaryRepository.java b/src/api/src/main/java/cn/iven/lianji/domain/repository/AnniversaryRepository.java
new file mode 100644
index 0000000..0cde3e0
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/domain/repository/AnniversaryRepository.java
@@ -0,0 +1,26 @@
+package cn.iven.lianji.domain.repository;
+
+import cn.iven.lianji.domain.model.entity.Anniversary;
+
+import java.time.LocalDate;
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 纪念日仓储接口。
+ */
+public interface AnniversaryRepository {
+
+    Anniversary save(Anniversary anniversary);
+
+    Optional<Anniversary> findById(Long id);
+
+    List<Anniversary> findByCoupleId(Long coupleId);
+
+    void deleteById(Long id);
+
+    /**
+     * 更新系统级纪念日的日期（级联更新恋爱开始日期时调用）。
+     */
+    void updateSystemAnniversaryDate(Long coupleId, LocalDate newDate);
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/converter/AnniversaryRepositoryConverter.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/converter/AnniversaryRepositoryConverter.java
new file mode 100644
index 0000000..a69fd24
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/converter/AnniversaryRepositoryConverter.java
@@ -0,0 +1,59 @@
+package cn.iven.lianji.infrastructure.repository.converter;
+
+import cn.iven.lianji.domain.model.entity.Anniversary;
+import cn.iven.lianji.domain.model.enumerate.RepeatType;
+import cn.iven.lianji.infrastructure.repository.dataobject.AnniversaryDO;
+import org.springframework.stereotype.Component;
+
+/**
+ * 纪念日仓库转换器。
+ * <p>负责 {@code Anniversary Entity ↔ AnniversaryDO} 的双向转换。</p>
+ */
+@Component
+public class AnniversaryRepositoryConverter {
+
+    public AnniversaryDO toDataObject(Anniversary entity) {
+        if (entity == null) {
+            return null;
+        }
+        return AnniversaryDO.builder()
+                .id(entity.getId())
+                .coupleId(entity.getCoupleId())
+                .title(entity.getTitle())
+                .anniversaryDate(entity.getDate())
+                .repeatType(entity.getRepeatType() != null ? entity.getRepeatType().name() : null)
+                .remindDays(entity.getRemindDays())
+                .isSystem(entity.getIsSystem())
+                .createdBy(entity.getCreatedBy())
+                .createdAt(entity.getCreatedAt())
+                .build();
+    }
+
+    public Anniversary toEntity(AnniversaryDO dataObject) {
+        if (dataObject == null) {
+            return null;
+        }
+        return Anniversary.builder()
+                .id(dataObject.getId())
+                .coupleId(dataObject.getCoupleId())
+                .title(dataObject.getTitle())
+                .date(dataObject.getAnniversaryDate())
+                .repeatType(parseRepeatType(dataObject.getRepeatType()))
+                .remindDays(dataObject.getRemindDays())
+                .isSystem(dataObject.getIsSystem())
+                .createdBy(dataObject.getCreatedBy())
+                .createdAt(dataObject.getCreatedAt())
+                .build();
+    }
+
+    private RepeatType parseRepeatType(String value) {
+        if (value == null) {
+            return null;
+        }
+        try {
+            return RepeatType.valueOf(value);
+        } catch (IllegalArgumentException e) {
+            return null;
+        }
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/AnniversaryDO.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/AnniversaryDO.java
new file mode 100644
index 0000000..5d83915
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/AnniversaryDO.java
@@ -0,0 +1,51 @@
+package cn.iven.lianji.infrastructure.repository.dataobject;
+
+import com.baomidou.mybatisplus.annotation.IdType;
+import com.baomidou.mybatisplus.annotation.TableId;
+import com.baomidou.mybatisplus.annotation.TableName;
+import lombok.Builder;
+import lombok.Data;
+
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+
+/**
+ * 纪念日数据持久化对象（DO）。
+ * <p>映射数据库表 {@code anniversary}，供 MyBatis-Plus 使用。</p>
+ */
+@Data
+@Builder
+@TableName("anniversary")
+public class AnniversaryDO {
+
+    /** 纪念日ID，主键自增 */
+    @TableId(type = IdType.AUTO)
+    private Long id;
+
+    /** 情侣关系ID */
+    private Long coupleId;
+
+    /** 纪念日标题 */
+    private String title;
+
+    /** 纪念日日期 */
+    private LocalDate anniversaryDate;
+
+    /** 重复类型：NONE/YEARLY/MONTHLY */
+    private String repeatType;
+
+    /** 提前提醒天数 */
+    private Integer remindDays;
+
+    /** 是否为系统级纪念日 */
+    private Boolean isSystem;
+
+    /** 创建者用户ID */
+    private Long createdBy;
+
+    /** 创建时间 */
+    private OffsetDateTime createdAt;
+
+    /** 更新时间 */
+    private OffsetDateTime updatedAt;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/impl/AnniversaryRepositoryImpl.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/impl/AnniversaryRepositoryImpl.java
new file mode 100644
index 0000000..d45c652
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/impl/AnniversaryRepositoryImpl.java
@@ -0,0 +1,63 @@
+package cn.iven.lianji.infrastructure.repository.impl;
+
+import cn.iven.lianji.domain.model.entity.Anniversary;
+import cn.iven.lianji.domain.repository.AnniversaryRepository;
+import cn.iven.lianji.infrastructure.repository.converter.AnniversaryRepositoryConverter;
+import cn.iven.lianji.infrastructure.repository.dataobject.AnniversaryDO;
+import cn.iven.lianji.infrastructure.repository.mapper.AnniversaryMapper;
+import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Repository;
+
+import java.time.LocalDate;
+import java.util.List;
+import java.util.Optional;
+
+/**
+ * 纪念日仓库实现。
+ * <p>基于 MyBatis-Plus 完成纪念日聚合的持久化操作。</p>
+ */
+@Repository
+@RequiredArgsConstructor
+public class AnniversaryRepositoryImpl implements AnniversaryRepository {
+
+    private final AnniversaryMapper anniversaryMapper;
+    private final AnniversaryRepositoryConverter converter;
+
+    @Override
+    public Anniversary save(Anniversary anniversary) {
+        AnniversaryDO dataObject = converter.toDataObject(anniversary);
+        if (dataObject.getId() == null) {
+            anniversaryMapper.insert(dataObject);
+        } else {
+            anniversaryMapper.updateById(dataObject);
+        }
+        return converter.toEntity(dataObject);
+    }
+
+    @Override
+    public Optional<Anniversary> findById(Long id) {
+        AnniversaryDO dataObject = anniversaryMapper.selectById(id);
+        return Optional.ofNullable(converter.toEntity(dataObject));
+    }
+
+    @Override
+    public List<Anniversary> findByCoupleId(Long coupleId) {
+        QueryWrapper<AnniversaryDO> wrapper = new QueryWrapper<>();
+        wrapper.eq("couple_id", coupleId);
+        wrapper.orderByAsc("anniversary_date");
+        return anniversaryMapper.selectList(wrapper).stream()
+                .map(converter::toEntity)
+                .toList();
+    }
+
+    @Override
+    public void deleteById(Long id) {
+        anniversaryMapper.deleteById(id);
+    }
+
+    @Override
+    public void updateSystemAnniversaryDate(Long coupleId, LocalDate newDate) {
+        anniversaryMapper.updateSystemAnniversaryDate(coupleId, newDate);
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/mapper/AnniversaryMapper.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/mapper/AnniversaryMapper.java
new file mode 100644
index 0000000..f2f115d
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/mapper/AnniversaryMapper.java
@@ -0,0 +1,28 @@
+package cn.iven.lianji.infrastructure.repository.mapper;
+
+import cn.iven.lianji.infrastructure.repository.dataobject.AnniversaryDO;
+import com.baomidou.mybatisplus.core.mapper.BaseMapper;
+import org.apache.ibatis.annotations.Mapper;
+import org.apache.ibatis.annotations.Param;
+import org.apache.ibatis.annotations.Update;
+
+import java.time.LocalDate;
+
+/**
+ * 纪念日 Mapper。
+ * <p>扩展 {@link BaseMapper} 提供通用 CRUD，额外提供系统级纪念日日期更新方法。</p>
+ */
+@Mapper
+public interface AnniversaryMapper extends BaseMapper<AnniversaryDO> {
+
+    /**
+     * 更新指定情侣的系统级纪念日日期。
+     *
+     * @param coupleId 情侣关系 ID
+     * @param newDate  新日期
+     * @return 更新行数
+     */
+    @Update("UPDATE anniversary SET anniversary_date = #{newDate}, updated_at = NOW() " +
+            "WHERE couple_id = #{coupleId} AND is_system = TRUE")
+    int updateSystemAnniversaryDate(@Param("coupleId") Long coupleId, @Param("newDate") LocalDate newDate);
+}
diff --git a/src/api/src/main/resources/application.yaml b/src/api/src/main/resources/application.yaml
index a126955..940381e 100644
--- a/src/api/src/main/resources/application.yaml
+++ b/src/api/src/main/resources/application.yaml
@@ -9,7 +9,7 @@ spring:
   data:
     redis:
       host: ${REDIS_HOST:localhost}
-      port: 6377
+      port: ${REDIS_PORT:6379}
       database: 0
       password: ${REDIS_PASS:}
       timeout: 5s
diff --git a/src/api/src/main/resources/db/migration/V2__add_anniversary_table.sql b/src/api/src/main/resources/db/migration/V2__add_anniversary_table.sql
new file mode 100644
index 0000000..a2813cf
--- /dev/null
+++ b/src/api/src/main/resources/db/migration/V2__add_anniversary_table.sql
@@ -0,0 +1,31 @@
+CREATE TABLE IF NOT EXISTS anniversary (
+    id BIGSERIAL PRIMARY KEY,
+    couple_id BIGINT NOT NULL,
+    title VARCHAR(100) NOT NULL,
+    anniversary_date DATE NOT NULL,
+    repeat_type VARCHAR(20) NOT NULL DEFAULT 'NONE',
+    remind_days INT,
+    is_system BOOLEAN NOT NULL DEFAULT FALSE,
+    created_by BIGINT,
+    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
+    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
+    CONSTRAINT fk_anniversary_couple FOREIGN KEY (couple_id) REFERENCES couple_relationship(id) ON DELETE CASCADE,
+    CONSTRAINT chk_anniversary_repeat_type CHECK (repeat_type IN ('NONE', 'YEARLY', 'MONTHLY'))
+);
+
+CREATE INDEX idx_anniversary_couple ON anniversary(couple_id);
+CREATE INDEX idx_anniversary_date ON anniversary(anniversary_date);
+
+-- Backfill system-level anniversaries for existing couple_relationship records
+INSERT INTO anniversary (couple_id, title, anniversary_date, repeat_type, remind_days, is_system)
+SELECT
+    id AS couple_id,
+    '恋爱开始日' AS title,
+    created_at::date AS anniversary_date,
+    'YEARLY' AS repeat_type,
+    3 AS remind_days,
+    TRUE AS is_system
+FROM couple_relationship
+WHERE NOT EXISTS (
+    SELECT 1 FROM anniversary a WHERE a.couple_id = couple_relationship.id AND a.is_system = TRUE
+);
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/remote/AnniversaryApi.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/remote/AnniversaryApi.kt
new file mode 100644
index 0000000..2bb2f58
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/remote/AnniversaryApi.kt
@@ -0,0 +1,89 @@
+/**
+ * 纪念日模块 Retrofit 接口
+ *
+ * 提供纪念日 CRUD 和即将到期查询接口。
+ */
+package cn.iven.app.feature.anniversary.data.remote
+
+import cn.iven.app.core.network.ApiResponse
+import kotlinx.serialization.Serializable
+import retrofit2.http.Body
+import retrofit2.http.DELETE
+import retrofit2.http.GET
+import retrofit2.http.POST
+import retrofit2.http.PUT
+import retrofit2.http.Path
+import retrofit2.http.Query
+
+interface AnniversaryApi {
+
+    /** 获取所有纪念日 */
+    @GET("api/v1/anniversaries")
+    suspend fun getAnniversaries(): ApiResponse<List<AnniversaryDto>>
+
+    /** 创建纪念日 */
+    @POST("api/v1/anniversaries")
+    suspend fun createAnniversary(@Body request: CreateAnniversaryRequestDto): ApiResponse<AnniversaryDto>
+
+    /** 更新纪念日 */
+    @PUT("api/v1/anniversaries/{id}")
+    suspend fun updateAnniversary(
+        @Path("id") id: Long,
+        @Body request: UpdateAnniversaryRequestDto
+    ): ApiResponse<AnniversaryDto>
+
+    /** 删除纪念日 */
+    @DELETE("api/v1/anniversaries/{id}")
+    suspend fun deleteAnniversary(@Path("id") id: Long): ApiResponse<Unit>
+
+    /** 根据 ID 获取单个纪念日 */
+    @GET("api/v1/anniversaries/{id}")
+    suspend fun getAnniversary(@Path("id") id: Long): ApiResponse<AnniversaryDto>
+
+    /** 获取即将到期的纪念日 */
+    @GET("api/v1/anniversaries/upcoming")
+    suspend fun getUpcomingAnniversaries(
+        @Query("limit") limit: Int = 3
+    ): ApiResponse<List<UpcomingAnniversaryDto>>
+}
+
+/** 纪念日响应 DTO */
+@Serializable
+data class AnniversaryDto(
+    val id: Long,
+    val coupleId: Long,
+    val title: String,
+    val date: String,
+    val repeatType: String,
+    val remindDays: Int? = null,
+    val isSystem: Boolean,
+    val createdBy: Long? = null
+)
+
+/** 创建纪念日请求 DTO */
+@Serializable
+data class CreateAnniversaryRequestDto(
+    val title: String,
+    val date: String,
+    val repeatType: String,
+    val remindDays: Int? = null
+)
+
+/** 更新纪念日请求 DTO */
+@Serializable
+data class UpdateAnniversaryRequestDto(
+    val title: String,
+    val date: String,
+    val repeatType: String,
+    val remindDays: Int? = null
+)
+
+/** 即将到期纪念日 DTO */
+@Serializable
+data class UpcomingAnniversaryDto(
+    val id: Long,
+    val title: String,
+    val date: String,
+    val repeatType: String,
+    val remainingDays: Int
+)
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/repository/AnniversaryRepositoryImpl.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/repository/AnniversaryRepositoryImpl.kt
new file mode 100644
index 0000000..08f7dc0
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/data/repository/AnniversaryRepositoryImpl.kt
@@ -0,0 +1,146 @@
+/**
+ * 纪念日仓库实现
+ *
+ * 负责调用远程纪念日接口并将 DTO 转换为领域层模型。
+ */
+package cn.iven.app.feature.anniversary.data.repository
+
+import cn.iven.app.feature.anniversary.data.remote.AnniversaryApi
+import cn.iven.app.feature.anniversary.data.remote.AnniversaryDto
+import cn.iven.app.feature.anniversary.data.remote.CreateAnniversaryRequestDto
+import cn.iven.app.feature.anniversary.data.remote.UpdateAnniversaryRequestDto
+import cn.iven.app.feature.anniversary.data.remote.UpcomingAnniversaryDto
+import cn.iven.app.feature.anniversary.domain.Anniversary
+import cn.iven.app.feature.anniversary.domain.AnniversaryRepository
+import cn.iven.app.feature.anniversary.domain.RepeatType
+import cn.iven.app.feature.anniversary.domain.UpcomingAnniversary
+import javax.inject.Inject
+
+class AnniversaryRepositoryImpl @Inject constructor(
+    private val api: AnniversaryApi
+) : AnniversaryRepository {
+
+    override suspend fun getAnniversaries(): Result<List<Anniversary>> {
+        return try {
+            val response = api.getAnniversaries()
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.map { it.toAnniversary() })
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    override suspend fun createAnniversary(
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary> {
+        return try {
+            val request = CreateAnniversaryRequestDto(
+                title = title,
+                date = date,
+                repeatType = repeatType.name,
+                remindDays = remindDays
+            )
+            val response = api.createAnniversary(request)
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.toAnniversary())
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    override suspend fun updateAnniversary(
+        id: Long,
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary> {
+        return try {
+            val request = UpdateAnniversaryRequestDto(
+                title = title,
+                date = date,
+                repeatType = repeatType.name,
+                remindDays = remindDays
+            )
+            val response = api.updateAnniversary(id, request)
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.toAnniversary())
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    override suspend fun deleteAnniversary(id: Long): Result<Unit> {
+        return try {
+            val response = api.deleteAnniversary(id)
+            if (response.isSuccess) {
+                Result.success(Unit)
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    override suspend fun getAnniversary(id: Long): Result<Anniversary> {
+        return try {
+            val response = api.getAnniversary(id)
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.toAnniversary())
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    override suspend fun getUpcomingAnniversaries(limit: Int): Result<List<UpcomingAnniversary>> {
+        return try {
+            val response = api.getUpcomingAnniversaries(limit)
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.map { it.toUpcomingAnniversary() })
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    private fun AnniversaryDto.toAnniversary(): Anniversary {
+        return Anniversary(
+            id = id,
+            coupleId = coupleId,
+            title = title,
+            date = date,
+            repeatType = RepeatType.fromString(repeatType),
+            remindDays = remindDays,
+            isSystem = isSystem,
+            createdBy = createdBy
+        )
+    }
+
+    private fun UpcomingAnniversaryDto.toUpcomingAnniversary(): UpcomingAnniversary {
+        return UpcomingAnniversary(
+            id = id,
+            title = title,
+            date = date,
+            repeatType = RepeatType.fromString(repeatType),
+            remainingDays = remainingDays
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/di/AnniversaryModule.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/di/AnniversaryModule.kt
new file mode 100644
index 0000000..0e4b8e4
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/di/AnniversaryModule.kt
@@ -0,0 +1,37 @@
+/**
+ * 纪念日模块依赖注入配置
+ *
+ * 绑定纪念日仓库接口实现，并提供纪念日 Retrofit API 实例。
+ */
+package cn.iven.app.feature.anniversary.di
+
+import cn.iven.app.feature.anniversary.data.remote.AnniversaryApi
+import cn.iven.app.feature.anniversary.data.repository.AnniversaryRepositoryImpl
+import cn.iven.app.feature.anniversary.domain.AnniversaryRepository
+import dagger.Binds
+import dagger.Module
+import dagger.Provides
+import dagger.hilt.InstallIn
+import dagger.hilt.components.SingletonComponent
+import retrofit2.Retrofit
+import javax.inject.Singleton
+
+@Module
+@InstallIn(SingletonComponent::class)
+abstract class AnniversaryModule {
+
+    /** 绑定 AnniversaryRepository 接口到 AnniversaryRepositoryImpl 实现 */
+    @Binds
+    @Singleton
+    abstract fun bindAnniversaryRepository(impl: AnniversaryRepositoryImpl): AnniversaryRepository
+
+    companion object {
+
+        /** 提供纪念日 Retrofit API */
+        @Provides
+        @Singleton
+        fun provideAnniversaryApi(retrofit: Retrofit): AnniversaryApi {
+            return retrofit.create(AnniversaryApi::class.java)
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/Anniversary.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/Anniversary.kt
new file mode 100644
index 0000000..6d8b7db
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/Anniversary.kt
@@ -0,0 +1,37 @@
+/**
+ * 纪念日领域模型
+ */
+package cn.iven.app.feature.anniversary.domain
+
+/** 纪念日 */
+data class Anniversary(
+    val id: Long,
+    val coupleId: Long,
+    val title: String,
+    val date: String,
+    val repeatType: RepeatType,
+    val remindDays: Int?,
+    val isSystem: Boolean,
+    val createdBy: Long?
+)
+
+/** 即将到期纪念日 */
+data class UpcomingAnniversary(
+    val id: Long,
+    val title: String,
+    val date: String,
+    val repeatType: RepeatType,
+    val remainingDays: Int
+)
+
+/** 重复类型 */
+enum class RepeatType(val label: String) {
+    NONE("一次性"),
+    YEARLY("每年"),
+    MONTHLY("每月");
+
+    companion object {
+        fun fromString(value: String): RepeatType =
+            entries.find { it.name == value } ?: NONE
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/AnniversaryRepository.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/AnniversaryRepository.kt
new file mode 100644
index 0000000..fef0329
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/AnniversaryRepository.kt
@@ -0,0 +1,38 @@
+/**
+ * 纪念日仓库接口
+ *
+ * 定义纪念日数据操作的领域层契约。
+ */
+package cn.iven.app.feature.anniversary.domain
+
+interface AnniversaryRepository {
+
+    /** 获取所有纪念日 */
+    suspend fun getAnniversaries(): Result<List<Anniversary>>
+
+    /** 创建纪念日 */
+    suspend fun createAnniversary(
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary>
+
+    /** 更新纪念日 */
+    suspend fun updateAnniversary(
+        id: Long,
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary>
+
+    /** 删除纪念日 */
+    suspend fun deleteAnniversary(id: Long): Result<Unit>
+
+    /** 获取即将到期的纪念日 */
+    suspend fun getUpcomingAnniversaries(limit: Int = 3): Result<List<UpcomingAnniversary>>
+
+    /** 根据 ID 获取单个纪念日 */
+    suspend fun getAnniversary(id: Long): Result<Anniversary>
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/CreateAnniversaryUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/CreateAnniversaryUseCase.kt
new file mode 100644
index 0000000..ddd93fb
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/CreateAnniversaryUseCase.kt
@@ -0,0 +1,20 @@
+/**
+ * 创建纪念日用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class CreateAnniversaryUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+
+    suspend operator fun invoke(
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary> {
+        return repository.createAnniversary(title, date, repeatType, remindDays)
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/DeleteAnniversaryUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/DeleteAnniversaryUseCase.kt
new file mode 100644
index 0000000..8741e8a
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/DeleteAnniversaryUseCase.kt
@@ -0,0 +1,15 @@
+/**
+ * 删除纪念日用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class DeleteAnniversaryUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+
+    suspend operator fun invoke(id: Long): Result<Unit> {
+        return repository.deleteAnniversary(id)
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversariesUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversariesUseCase.kt
new file mode 100644
index 0000000..e6ff8f1
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversariesUseCase.kt
@@ -0,0 +1,15 @@
+/**
+ * 获取所有纪念日用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class GetAnniversariesUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+
+    suspend operator fun invoke(): Result<List<Anniversary>> {
+        return repository.getAnniversaries()
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversaryByIdUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversaryByIdUseCase.kt
new file mode 100644
index 0000000..e12f67a
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetAnniversaryByIdUseCase.kt
@@ -0,0 +1,11 @@
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class GetAnniversaryByIdUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+    suspend operator fun invoke(id: Long): Result<Anniversary> {
+        return repository.getAnniversary(id)
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetUpcomingAnniversariesUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetUpcomingAnniversariesUseCase.kt
new file mode 100644
index 0000000..52cae07
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/GetUpcomingAnniversariesUseCase.kt
@@ -0,0 +1,15 @@
+/**
+ * 获取即将到期纪念日用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class GetUpcomingAnniversariesUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+
+    suspend operator fun invoke(limit: Int = 3): Result<List<UpcomingAnniversary>> {
+        return repository.getUpcomingAnniversaries(limit)
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateAnniversaryUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateAnniversaryUseCase.kt
new file mode 100644
index 0000000..37a1474
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateAnniversaryUseCase.kt
@@ -0,0 +1,21 @@
+/**
+ * 更新纪念日用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import javax.inject.Inject
+
+class UpdateAnniversaryUseCase @Inject constructor(
+    private val repository: AnniversaryRepository
+) {
+
+    suspend operator fun invoke(
+        id: Long,
+        title: String,
+        date: String,
+        repeatType: RepeatType,
+        remindDays: Int?
+    ): Result<Anniversary> {
+        return repository.updateAnniversary(id, title, date, repeatType, remindDays)
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateCoupleStartDateUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateCoupleStartDateUseCase.kt
new file mode 100644
index 0000000..b97428a
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/domain/UpdateCoupleStartDateUseCase.kt
@@ -0,0 +1,26 @@
+/**
+ * 更新情侣开始日期用例
+ */
+package cn.iven.app.feature.anniversary.domain
+
+import cn.iven.app.feature.auth.data.remote.CoupleApi
+import cn.iven.app.feature.auth.data.remote.UpdateStartDateRequestDto
+import javax.inject.Inject
+
+class UpdateCoupleStartDateUseCase @Inject constructor(
+    private val coupleApi: CoupleApi
+) {
+
+    suspend operator fun invoke(date: String): Result<Unit> {
+        return try {
+            val response = coupleApi.updateStartDate(UpdateStartDateRequestDto(date))
+            if (response.isSuccess) {
+                Result.success(Unit)
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditContent.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditContent.kt
new file mode 100644
index 0000000..d801339
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditContent.kt
@@ -0,0 +1,386 @@
+package cn.iven.app.feature.anniversary.ui.edit
+
+import android.app.DatePickerDialog
+import androidx.compose.foundation.background
+import androidx.compose.foundation.border
+import androidx.compose.foundation.clickable
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
+import androidx.compose.foundation.layout.fillMaxSize
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.height
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
+import androidx.compose.foundation.rememberScrollState
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.foundation.text.BasicTextField
+import androidx.compose.foundation.verticalScroll
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.automirrored.filled.ArrowBack
+import androidx.compose.material.icons.filled.CalendarToday
+import androidx.compose.material3.CircularProgressIndicator
+import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.Icon
+import androidx.compose.material3.IconButton
+import androidx.compose.material3.Scaffold
+import androidx.compose.material3.Text
+import androidx.compose.material3.TopAppBar
+import androidx.compose.material3.TopAppBarDefaults
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.platform.LocalContext
+import androidx.compose.ui.text.TextStyle
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.tooling.preview.Preview
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.feature.anniversary.domain.RepeatType
+import cn.iven.app.ui.theme.BackgroundLight
+import cn.iven.app.ui.theme.DividerLight
+import cn.iven.app.ui.theme.Error
+import cn.iven.app.ui.theme.LianjiTheme
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextDisabledLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import cn.iven.app.ui.theme.TextSecondaryLight
+import java.time.LocalDate
+import java.time.format.DateTimeFormatter
+import java.util.Calendar
+
+@OptIn(ExperimentalMaterial3Api::class)
+@Composable
+fun AnniversaryEditContent(
+    formState: AnniversaryFormState,
+    submitState: AnniversaryEditUiState,
+    loadState: AnniversaryEditUiState,
+    onEvent: (AnniversaryEditUiEvent) -> Unit,
+    onNavigateBack: () -> Unit,
+    modifier: Modifier = Modifier
+) {
+    val context = LocalContext.current
+    val title = when {
+        formState.isSystem -> "纪念日详情"
+        formState.isEditMode -> "编辑纪念日"
+        else -> "新建纪念日"
+    }
+    val readOnly = formState.isSystem
+
+    Scaffold(
+        modifier = modifier,
+        topBar = {
+            TopAppBar(
+                title = {
+                    Text(
+                        text = title,
+                        fontSize = 20.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
+                    )
+                },
+                navigationIcon = {
+                    IconButton(onClick = onNavigateBack) {
+                        Icon(
+                            imageVector = Icons.AutoMirrored.Filled.ArrowBack,
+                            contentDescription = "返回",
+                            tint = TextPrimaryLight
+                        )
+                    }
+                },
+                colors = TopAppBarDefaults.topAppBarColors(
+                    containerColor = BackgroundLight
+                )
+            )
+        }
+    ) { paddingValues ->
+        Column(
+            modifier = Modifier
+                .fillMaxSize()
+                .background(BackgroundLight)
+                .padding(paddingValues)
+                .padding(horizontal = 24.dp)
+                .verticalScroll(rememberScrollState()),
+            verticalArrangement = Arrangement.spacedBy(24.dp)
+        ) {
+            Spacer(modifier = Modifier.height(8.dp))
+
+            if (loadState is AnniversaryEditUiState.Loading) {
+                Box(
+                    modifier = Modifier.fillMaxWidth().height(200.dp),
+                    contentAlignment = Alignment.Center
+                ) {
+                    CircularProgressIndicator(color = LovePink)
+                }
+            } else if (loadState is AnniversaryEditUiState.Error) {
+                Box(
+                    modifier = Modifier.fillMaxWidth().height(200.dp),
+                    contentAlignment = Alignment.Center
+                ) {
+                    Text(
+                        text = loadState.message,
+                        fontSize = 14.sp,
+                        color = Error
+                    )
+                }
+            } else {
+                if (readOnly) {
+                    Text(
+                        text = "系统纪念日不可修改",
+                        fontSize = 13.sp,
+                        color = LovePink,
+                        modifier = Modifier.padding(start = 4.dp)
+                    )
+                }
+
+                // Title input
+                FormSection(label = "标题") {
+                    BasicTextField(
+                        value = formState.title,
+                        onValueChange = { if (!readOnly) onEvent(AnniversaryEditUiEvent.TitleChanged(it)) },
+                        modifier = Modifier.fillMaxWidth(),
+                        singleLine = true,
+                        enabled = !readOnly,
+                        readOnly = readOnly,
+                        textStyle = TextStyle(
+                            fontSize = 15.sp,
+                            color = TextPrimaryLight
+                        ),
+                        decorationBox = { innerTextField ->
+                            Box(
+                                modifier = Modifier
+                                    .fillMaxWidth()
+                                    .height(52.dp)
+                                    .clip(RoundedCornerShape(12.dp))
+                                    .background(SurfaceLight)
+                                    .border(1.dp, DividerLight, RoundedCornerShape(12.dp))
+                                    .padding(horizontal = 16.dp),
+                                contentAlignment = Alignment.CenterStart
+                            ) {
+                                if (formState.title.isEmpty()) {
+                                    Text(
+                                        text = "输入纪念日标题...",
+                                        fontSize = 15.sp,
+                                        color = TextDisabledLight
+                                    )
+                                }
+                                innerTextField()
+                            }
+                        }
+                    )
+                }
+
+                // Date picker
+                FormSection(label = "日期") {
+                    val datePickerDialog = DatePickerDialog(
+                        context,
+                        { _, year, month, dayOfMonth ->
+                            val date = LocalDate.of(year, month + 1, dayOfMonth)
+                                .format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))
+                            onEvent(AnniversaryEditUiEvent.DateChanged(date))
+                        },
+                        Calendar.getInstance().get(Calendar.YEAR),
+                        Calendar.getInstance().get(Calendar.MONTH),
+                        Calendar.getInstance().get(Calendar.DAY_OF_MONTH)
+                    )
+
+                    if (formState.date.isNotBlank()) {
+                        try {
+                            val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
+                            val date = LocalDate.parse(formState.date, formatter)
+                            datePickerDialog.updateDate(date.year, date.monthValue - 1, date.dayOfMonth)
+                        } catch (_: Exception) { }
+                    }
+
+                    Row(
+                        modifier = Modifier
+                            .fillMaxWidth()
+                            .height(52.dp)
+                            .clip(RoundedCornerShape(12.dp))
+                            .background(SurfaceLight)
+                            .border(1.dp, DividerLight, RoundedCornerShape(12.dp))
+                            .clickable(enabled = !readOnly) { datePickerDialog.show() }
+                            .padding(horizontal = 16.dp),
+                        verticalAlignment = Alignment.CenterVertically,
+                        horizontalArrangement = Arrangement.SpaceBetween
+                    ) {
+                        Text(
+                            text = formState.date.ifEmpty { "选择日期" },
+                            fontSize = 15.sp,
+                            color = if (formState.date.isEmpty()) TextDisabledLight else TextPrimaryLight
+                        )
+                        Icon(
+                            imageVector = Icons.Default.CalendarToday,
+                            contentDescription = null,
+                            modifier = Modifier.size(20.dp),
+                            tint = TextSecondaryLight
+                        )
+                    }
+                }
+
+                // Repeat type selector
+                FormSection(label = "重复") {
+                    Row(
+                        modifier = Modifier.fillMaxWidth(),
+                        horizontalArrangement = Arrangement.spacedBy(8.dp)
+                    ) {
+                        RepeatType.entries.forEach { type ->
+                            val selected = formState.repeatType == type
+                            Box(
+                                modifier = Modifier
+                                    .weight(1f)
+                                    .height(44.dp)
+                                    .clip(RoundedCornerShape(10.dp))
+                                    .background(if (selected) LovePink else SurfaceLight)
+                                    .border(
+                                        width = 1.dp,
+                                        color = if (selected) LovePink else DividerLight,
+                                        shape = RoundedCornerShape(10.dp)
+                                    )
+                                    .clickable(enabled = !readOnly) { onEvent(AnniversaryEditUiEvent.RepeatTypeChanged(type)) },
+                                contentAlignment = Alignment.Center
+                            ) {
+                                Text(
+                                    text = type.label,
+                                    fontSize = 14.sp,
+                                    fontWeight = FontWeight.Medium,
+                                    color = if (selected) SurfaceLight else TextPrimaryLight
+                                )
+                            }
+                        }
+                    }
+                }
+
+                // Remind days selector
+                FormSection(label = "提醒") {
+                    val remindOptions = listOf(
+                        null to "不提醒",
+                        0 to "当天",
+                        1 to "1天前",
+                        3 to "3天前",
+                        7 to "7天前"
+                    )
+                    Row(
+                        modifier = Modifier.fillMaxWidth(),
+                        horizontalArrangement = Arrangement.spacedBy(8.dp)
+                    ) {
+                        remindOptions.forEach { (days, label) ->
+                            val selected = formState.remindDays == days
+                            Box(
+                                modifier = Modifier
+                                    .height(36.dp)
+                                    .clip(RoundedCornerShape(8.dp))
+                                    .background(if (selected) LovePinkLight else SurfaceLight)
+                                    .border(
+                                        width = 1.dp,
+                                        color = if (selected) LovePink else DividerLight,
+                                        shape = RoundedCornerShape(8.dp)
+                                    )
+                                    .clickable(enabled = !readOnly) { onEvent(AnniversaryEditUiEvent.RemindDaysChanged(days)) }
+                                    .padding(horizontal = 14.dp),
+                                contentAlignment = Alignment.Center
+                            ) {
+                                Text(
+                                    text = label,
+                                    fontSize = 13.sp,
+                                    fontWeight = FontWeight.Medium,
+                                    color = if (selected) LovePink else TextPrimaryLight
+                                )
+                            }
+                        }
+                    }
+                }
+
+                if (submitState is AnniversaryEditUiState.Error) {
+                    Text(
+                        text = submitState.message,
+                        fontSize = 13.sp,
+                        color = Error,
+                        modifier = Modifier.padding(start = 4.dp)
+                    )
+                }
+
+                Spacer(modifier = Modifier.height(8.dp))
+
+                if (!readOnly) {
+                    Box(
+                        modifier = Modifier
+                            .fillMaxWidth()
+                            .height(52.dp)
+                            .clip(RoundedCornerShape(14.dp))
+                            .background(
+                                if (formState.isValid) LovePink else LovePink.copy(alpha = 0.5f)
+                            )
+                            .clickable(
+                                enabled = formState.isValid && submitState != AnniversaryEditUiState.Loading
+                            ) {
+                                onEvent(AnniversaryEditUiEvent.Submit)
+                            },
+                        contentAlignment = Alignment.Center
+                    ) {
+                        if (submitState is AnniversaryEditUiState.Loading) {
+                            CircularProgressIndicator(
+                                modifier = Modifier.size(24.dp),
+                                color = SurfaceLight,
+                                strokeWidth = 2.dp
+                            )
+                        } else {
+                            Text(
+                                text = if (formState.isEditMode) "保存修改" else "创建纪念日",
+                                fontSize = 16.sp,
+                                fontWeight = FontWeight.SemiBold,
+                                color = SurfaceLight
+                            )
+                        }
+                    }
+                }
+
+                Spacer(modifier = Modifier.height(24.dp))
+            }
+        }
+    }
+}
+
+@Composable
+private fun FormSection(
+    label: String,
+    modifier: Modifier = Modifier,
+    content: @Composable () -> Unit
+) {
+    Column(
+        modifier = modifier.fillMaxWidth(),
+        verticalArrangement = Arrangement.spacedBy(10.dp)
+    ) {
+        Text(
+            text = label,
+            fontSize = 14.sp,
+            fontWeight = FontWeight.Medium,
+            color = TextPrimaryLight
+        )
+        content()
+    }
+}
+
+@Preview(showBackground = true)
+@Composable
+private fun AnniversaryEditContentPreview() {
+    LianjiTheme {
+        AnniversaryEditContent(
+            formState = AnniversaryFormState(
+                title = "恋爱一周年",
+                date = "2024-05-20",
+                repeatType = RepeatType.YEARLY,
+                remindDays = 7
+            ),
+            submitState = AnniversaryEditUiState.Idle,
+            loadState = AnniversaryEditUiState.Idle,
+            onEvent = {},
+            onNavigateBack = {}
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditScreen.kt
new file mode 100644
index 0000000..7acb865
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditScreen.kt
@@ -0,0 +1,41 @@
+package cn.iven.app.feature.anniversary.ui.edit
+
+import androidx.compose.runtime.Composable
+import androidx.compose.runtime.LaunchedEffect
+import androidx.compose.runtime.getValue
+import androidx.hilt.navigation.compose.hiltViewModel
+import androidx.lifecycle.compose.collectAsStateWithLifecycle
+
+@Composable
+fun AnniversaryEditScreen(
+    anniversaryId: Long? = null,
+    onSaveSuccess: () -> Unit,
+    onNavigateBack: () -> Unit,
+    viewModel: AnniversaryEditViewModel = hiltViewModel()
+) {
+    val formState by viewModel.formState.collectAsStateWithLifecycle()
+    val submitState by viewModel.submitState.collectAsStateWithLifecycle()
+    val loadState by viewModel.loadState.collectAsStateWithLifecycle()
+
+    LaunchedEffect(anniversaryId) {
+        if (anniversaryId != null) {
+            viewModel.loadById(anniversaryId)
+        } else {
+            viewModel.initNew()
+        }
+    }
+
+    LaunchedEffect(submitState) {
+        if (submitState is AnniversaryEditUiState.Success) {
+            onSaveSuccess()
+        }
+    }
+
+    AnniversaryEditContent(
+        formState = formState,
+        submitState = submitState,
+        loadState = loadState,
+        onEvent = viewModel::onEvent,
+        onNavigateBack = onNavigateBack
+    )
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiEvent.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiEvent.kt
new file mode 100644
index 0000000..d3ff04e
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiEvent.kt
@@ -0,0 +1,9 @@
+package cn.iven.app.feature.anniversary.ui.edit
+
+sealed interface AnniversaryEditUiEvent {
+    data class TitleChanged(val title: String) : AnniversaryEditUiEvent
+    data class DateChanged(val date: String) : AnniversaryEditUiEvent
+    data class RepeatTypeChanged(val repeatType: cn.iven.app.feature.anniversary.domain.RepeatType) : AnniversaryEditUiEvent
+    data class RemindDaysChanged(val remindDays: Int?) : AnniversaryEditUiEvent
+    data object Submit : AnniversaryEditUiEvent
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiState.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiState.kt
new file mode 100644
index 0000000..ef3fd75
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditUiState.kt
@@ -0,0 +1,20 @@
+package cn.iven.app.feature.anniversary.ui.edit
+
+sealed interface AnniversaryEditUiState {
+    data object Idle : AnniversaryEditUiState
+    data object Loading : AnniversaryEditUiState
+    data object Success : AnniversaryEditUiState
+    data class Error(val message: String) : AnniversaryEditUiState
+}
+
+data class AnniversaryFormState(
+    val title: String = "",
+    val date: String = "",
+    val repeatType: cn.iven.app.feature.anniversary.domain.RepeatType = cn.iven.app.feature.anniversary.domain.RepeatType.NONE,
+    val remindDays: Int? = null,
+    val isEditMode: Boolean = false,
+    val anniversaryId: Long? = null,
+    val isSystem: Boolean = false
+) {
+    val isValid: Boolean get() = title.isNotBlank() && date.isNotBlank() && !isSystem
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditViewModel.kt
new file mode 100644
index 0000000..4ff66d3
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/edit/AnniversaryEditViewModel.kt
@@ -0,0 +1,121 @@
+package cn.iven.app.feature.anniversary.ui.edit
+
+import androidx.lifecycle.ViewModel
+import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.anniversary.domain.Anniversary
+import cn.iven.app.feature.anniversary.domain.CreateAnniversaryUseCase
+import cn.iven.app.feature.anniversary.domain.GetAnniversaryByIdUseCase
+import cn.iven.app.feature.anniversary.domain.RepeatType
+import cn.iven.app.feature.anniversary.domain.UpdateAnniversaryUseCase
+import dagger.hilt.android.lifecycle.HiltViewModel
+import kotlinx.coroutines.flow.MutableStateFlow
+import kotlinx.coroutines.flow.StateFlow
+import kotlinx.coroutines.flow.asStateFlow
+import kotlinx.coroutines.flow.update
+import kotlinx.coroutines.launch
+import java.time.LocalDate
+import java.time.format.DateTimeFormatter
+import javax.inject.Inject
+
+@HiltViewModel
+class AnniversaryEditViewModel @Inject constructor(
+    private val createAnniversaryUseCase: CreateAnniversaryUseCase,
+    private val updateAnniversaryUseCase: UpdateAnniversaryUseCase,
+    private val getAnniversaryByIdUseCase: GetAnniversaryByIdUseCase
+) : ViewModel() {
+
+    private val _formState = MutableStateFlow(AnniversaryFormState())
+    val formState: StateFlow<AnniversaryFormState> = _formState.asStateFlow()
+
+    private val _submitState = MutableStateFlow<AnniversaryEditUiState>(AnniversaryEditUiState.Idle)
+    val submitState: StateFlow<AnniversaryEditUiState> = _submitState.asStateFlow()
+
+    private val _loadState = MutableStateFlow<AnniversaryEditUiState>(AnniversaryEditUiState.Idle)
+    val loadState: StateFlow<AnniversaryEditUiState> = _loadState.asStateFlow()
+
+    /** 初始化新建模式 */
+    fun initNew() {
+        _formState.value = AnniversaryFormState(
+            date = LocalDate.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd"))
+        )
+        _submitState.value = AnniversaryEditUiState.Idle
+        _loadState.value = AnniversaryEditUiState.Idle
+    }
+
+    /** 根据 ID 加载纪念日数据（编辑模式） */
+    fun loadById(id: Long) {
+        viewModelScope.launch {
+            _loadState.value = AnniversaryEditUiState.Loading
+            val result = getAnniversaryByIdUseCase(id)
+            if (result.isSuccess) {
+                val anniversary = result.getOrThrow()
+                _formState.value = AnniversaryFormState(
+                    title = anniversary.title,
+                    date = anniversary.date,
+                    repeatType = anniversary.repeatType,
+                    remindDays = anniversary.remindDays,
+                    isEditMode = true,
+                    anniversaryId = anniversary.id,
+                    isSystem = anniversary.isSystem
+                )
+                _loadState.value = AnniversaryEditUiState.Idle
+            } else {
+                _loadState.value = AnniversaryEditUiState.Error(
+                    result.exceptionOrNull()?.message ?: "加载失败"
+                )
+            }
+            _submitState.value = AnniversaryEditUiState.Idle
+        }
+    }
+
+    fun onEvent(event: AnniversaryEditUiEvent) {
+        when (event) {
+            is AnniversaryEditUiEvent.TitleChanged -> {
+                _formState.update { it.copy(title = event.title) }
+            }
+            is AnniversaryEditUiEvent.DateChanged -> {
+                _formState.update { it.copy(date = event.date) }
+            }
+            is AnniversaryEditUiEvent.RepeatTypeChanged -> {
+                _formState.update { it.copy(repeatType = event.repeatType) }
+            }
+            is AnniversaryEditUiEvent.RemindDaysChanged -> {
+                _formState.update { it.copy(remindDays = event.remindDays) }
+            }
+            is AnniversaryEditUiEvent.Submit -> submit()
+        }
+    }
+
+    private fun submit() {
+        val form = _formState.value
+        if (!form.isValid) {
+            _submitState.value = AnniversaryEditUiState.Error("请填写完整信息")
+            return
+        }
+
+        viewModelScope.launch {
+            _submitState.value = AnniversaryEditUiState.Loading
+            val result = if (form.isEditMode && form.anniversaryId != null) {
+                updateAnniversaryUseCase(
+                    id = form.anniversaryId,
+                    title = form.title,
+                    date = form.date,
+                    repeatType = form.repeatType,
+                    remindDays = form.remindDays
+                )
+            } else {
+                createAnniversaryUseCase(
+                    title = form.title,
+                    date = form.date,
+                    repeatType = form.repeatType,
+                    remindDays = form.remindDays
+                )
+            }
+            _submitState.value = if (result.isSuccess) {
+                AnniversaryEditUiState.Success
+            } else {
+                AnniversaryEditUiState.Error(result.exceptionOrNull()?.message ?: "保存失败")
+            }
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt
new file mode 100644
index 0000000..be7d822
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListContent.kt
@@ -0,0 +1,463 @@
+package cn.iven.app.feature.anniversary.ui.list
+
+import androidx.compose.foundation.background
+import androidx.compose.foundation.border
+import androidx.compose.foundation.clickable
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.PaddingValues
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
+import androidx.compose.foundation.layout.fillMaxSize
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
+import androidx.compose.foundation.layout.width
+import androidx.compose.foundation.lazy.LazyColumn
+import androidx.compose.foundation.lazy.items
+import androidx.compose.foundation.shape.CircleShape
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.filled.Add
+import androidx.compose.material.icons.filled.Delete
+import androidx.compose.material.icons.filled.Favorite
+import androidx.compose.material3.Card
+import androidx.compose.material3.CardDefaults
+import androidx.compose.material3.CircularProgressIndicator
+import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.FloatingActionButton
+import androidx.compose.material3.Icon
+import androidx.compose.material3.IconButton
+import androidx.compose.material3.Text
+import androidx.compose.material3.TopAppBar
+import androidx.compose.material3.TopAppBarDefaults
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.tooling.preview.Preview
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.feature.anniversary.domain.Anniversary
+import cn.iven.app.feature.anniversary.domain.RepeatType
+import cn.iven.app.ui.theme.BackgroundLight
+import cn.iven.app.ui.theme.DividerLight
+import cn.iven.app.ui.theme.LianjiTheme
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import cn.iven.app.ui.theme.TextSecondaryLight
+import com.google.accompanist.swiperefresh.SwipeRefresh
+import com.google.accompanist.swiperefresh.SwipeRefreshIndicator
+import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
+import java.time.LocalDate
+import java.time.format.DateTimeFormatter
+import java.time.temporal.ChronoUnit
+
+@OptIn(ExperimentalMaterial3Api::class)
+@Composable
+fun AnniversaryListContent(
+    uiState: AnniversaryListUiState,
+    onEvent: (AnniversaryListUiEvent) -> Unit,
+    modifier: Modifier = Modifier
+) {
+    val isRefreshing = uiState is AnniversaryListUiState.Loading
+    val swipeRefreshState = rememberSwipeRefreshState(isRefreshing)
+
+    Box(modifier = modifier.fillMaxSize()) {
+        Column(
+            modifier = Modifier
+                .fillMaxSize()
+                .background(BackgroundLight)
+        ) {
+            TopAppBar(
+                title = {
+                    Text(
+                        text = "纪念日",
+                        fontSize = 20.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
+                    )
+                },
+                colors = TopAppBarDefaults.topAppBarColors(
+                    containerColor = BackgroundLight
+                )
+            )
+
+            SwipeRefresh(
+                state = swipeRefreshState,
+                onRefresh = { onEvent(AnniversaryListUiEvent.Refresh) },
+                indicator = { state, trigger ->
+                    SwipeRefreshIndicator(
+                        state = state,
+                        refreshTriggerDistance = trigger,
+                        contentColor = LovePink
+                    )
+                }
+            ) {
+                when (val state = uiState) {
+                    is AnniversaryListUiState.Loading -> {
+                        Box(
+                            modifier = Modifier.fillMaxSize(),
+                            contentAlignment = Alignment.Center
+                        ) {
+                            CircularProgressIndicator(color = LovePink)
+                        }
+                    }
+
+                    is AnniversaryListUiState.Error -> {
+                        ErrorState(
+                            message = state.message,
+                            onRetry = { onEvent(AnniversaryListUiEvent.Refresh) }
+                        )
+                    }
+
+                    is AnniversaryListUiState.Empty -> {
+                        EmptyState(
+                            onCreateClick = { onEvent(AnniversaryListUiEvent.CreateClick) }
+                        )
+                    }
+
+                    is AnniversaryListUiState.Success -> {
+                        Column(modifier = Modifier.fillMaxSize()) {
+                            FilterChipsRow(
+                                selectedFilter = state.filter,
+                                onFilterSelected = {
+                                    onEvent(AnniversaryListUiEvent.FilterChanged(it))
+                                }
+                            )
+                            LazyColumn(
+                                modifier = Modifier.fillMaxSize(),
+                                contentPadding = PaddingValues(16.dp),
+                                verticalArrangement = Arrangement.spacedBy(12.dp)
+                            ) {
+                                items(state.anniversaries) { anniversary ->
+                                    AnniversaryListItem(
+                                        anniversary = anniversary,
+                                        onEditClick = {
+                                            if (!anniversary.isSystem) {
+                                                onEvent(AnniversaryListUiEvent.EditClick(anniversary.id))
+                                            }
+                                        },
+                                        onDeleteClick = {
+                                            onEvent(AnniversaryListUiEvent.DeleteClick(anniversary.id))
+                                        }
+                                    )
+                                }
+                            }
+                        }
+                    }
+                }
+            }
+        }
+
+        // FAB positioned absolutely to avoid Scaffold nesting issues
+        if (uiState is AnniversaryListUiState.Success || uiState is AnniversaryListUiState.Empty) {
+            FloatingActionButton(
+                onClick = { onEvent(AnniversaryListUiEvent.CreateClick) },
+                containerColor = LovePink,
+                shape = CircleShape,
+                modifier = Modifier
+                    .align(Alignment.BottomEnd)
+                    .padding(end = 24.dp, bottom = 48.dp)
+            ) {
+                Icon(
+                    imageVector = Icons.Default.Add,
+                    contentDescription = "添加纪念日",
+                    tint = SurfaceLight
+                )
+            }
+        }
+    }
+}
+
+@Composable
+private fun FilterChipsRow(
+    selectedFilter: RepeatTypeFilter,
+    onFilterSelected: (RepeatTypeFilter) -> Unit,
+    modifier: Modifier = Modifier
+) {
+    Row(
+        modifier = modifier
+            .fillMaxWidth()
+            .padding(horizontal = 16.dp, vertical = 8.dp),
+        horizontalArrangement = Arrangement.spacedBy(8.dp)
+    ) {
+        RepeatTypeFilter.entries.forEach { filter ->
+            val selected = filter == selectedFilter
+            Box(
+                modifier = Modifier
+                    .clip(RoundedCornerShape(16.dp))
+                    .background(if (selected) LovePink else SurfaceLight)
+                    .border(
+                        width = 1.dp,
+                        color = if (selected) LovePink else DividerLight,
+                        shape = RoundedCornerShape(16.dp)
+                    )
+                    .clickable { onFilterSelected(filter) }
+                    .padding(horizontal = 16.dp, vertical = 8.dp)
+            ) {
+                Text(
+                    text = filter.label,
+                    fontSize = 13.sp,
+                    fontWeight = FontWeight.Medium,
+                    color = if (selected) SurfaceLight else TextPrimaryLight
+                )
+            }
+        }
+    }
+}
+
+@Composable
+private fun AnniversaryListItem(
+    anniversary: Anniversary,
+    onEditClick: () -> Unit,
+    onDeleteClick: () -> Unit,
+    modifier: Modifier = Modifier
+) {
+    val remainingDays = calculateRemainingDays(anniversary.date, anniversary.repeatType)
+    val isUpcoming = remainingDays != null && remainingDays >= 0
+
+    Card(
+        modifier = modifier
+            .fillMaxWidth()
+            .clickable(onClick = onEditClick),
+        colors = CardDefaults.cardColors(containerColor = SurfaceLight),
+        shape = RoundedCornerShape(12.dp)
+    ) {
+        Row(
+            modifier = Modifier
+                .fillMaxWidth()
+                .padding(16.dp),
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            Box(
+                modifier = Modifier
+                    .size(44.dp)
+                    .clip(CircleShape)
+                    .background(if (anniversary.isSystem) LovePinkLight else DividerLight),
+                contentAlignment = Alignment.Center
+            ) {
+                Icon(
+                    imageVector = Icons.Default.Favorite,
+                    contentDescription = null,
+                    modifier = Modifier.size(22.dp),
+                    tint = if (anniversary.isSystem) LovePink else TextSecondaryLight
+                )
+            }
+
+            Spacer(modifier = Modifier.width(12.dp))
+
+            Column(
+                modifier = Modifier.weight(1f),
+                verticalArrangement = Arrangement.spacedBy(4.dp)
+            ) {
+                Row(
+                    verticalAlignment = Alignment.CenterVertically,
+                    horizontalArrangement = Arrangement.spacedBy(6.dp)
+                ) {
+                    Text(
+                        text = anniversary.title,
+                        fontSize = 15.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
+                    )
+                    if (anniversary.isSystem) {
+                        Box(
+                            modifier = Modifier
+                                .clip(RoundedCornerShape(4.dp))
+                                .background(LovePinkLight)
+                                .padding(horizontal = 6.dp, vertical = 2.dp)
+                        ) {
+                            Text(
+                                text = "系统",
+                                fontSize = 10.sp,
+                                color = LovePink
+                            )
+                        }
+                    }
+                }
+                Text(
+                    text = "${anniversary.date}  ·  ${anniversary.repeatType.label}",
+                    fontSize = 13.sp,
+                    color = TextSecondaryLight
+                )
+            }
+
+            if (remainingDays != null) {
+                Box(
+                    modifier = Modifier
+                        .clip(RoundedCornerShape(8.dp))
+                        .background(if (isUpcoming) LovePinkLight else DividerLight)
+                        .padding(horizontal = 10.dp, vertical = 6.dp)
+                ) {
+                    Text(
+                        text = if (remainingDays == 0) "今天" else "${remainingDays}天",
+                        fontSize = 12.sp,
+                        fontWeight = FontWeight.Medium,
+                        color = if (isUpcoming) LovePink else TextSecondaryLight
+                    )
+                }
+            }
+
+            if (!anniversary.isSystem) {
+                IconButton(onClick = onDeleteClick) {
+                    Icon(
+                        imageVector = Icons.Default.Delete,
+                        contentDescription = "删除",
+                        modifier = Modifier.size(18.dp),
+                        tint = TextSecondaryLight
+                    )
+                }
+            }
+        }
+    }
+}
+
+@Composable
+private fun EmptyState(
+    onCreateClick: () -> Unit,
+    modifier: Modifier = Modifier
+) {
+    Box(
+        modifier = modifier.fillMaxSize(),
+        contentAlignment = Alignment.Center
+    ) {
+        Column(
+            horizontalAlignment = Alignment.CenterHorizontally,
+            verticalArrangement = Arrangement.spacedBy(16.dp)
+        ) {
+            Icon(
+                imageVector = Icons.Default.Favorite,
+                contentDescription = null,
+                modifier = Modifier.size(64.dp),
+                tint = LovePinkLight
+            )
+            Text(
+                text = "还没有纪念日",
+                fontSize = 16.sp,
+                fontWeight = FontWeight.Medium,
+                color = TextSecondaryLight
+            )
+            Box(
+                modifier = Modifier
+                    .clip(RoundedCornerShape(12.dp))
+                    .background(LovePink)
+                    .clickable(onClick = onCreateClick)
+                    .padding(horizontal = 24.dp, vertical = 12.dp)
+            ) {
+                Text(
+                    text = "添加第一个纪念日",
+                    fontSize = 14.sp,
+                    fontWeight = FontWeight.SemiBold,
+                    color = SurfaceLight
+                )
+            }
+        }
+    }
+}
+
+@Composable
+private fun ErrorState(
+    message: String,
+    onRetry: () -> Unit,
+    modifier: Modifier = Modifier
+) {
+    Box(
+        modifier = modifier.fillMaxSize(),
+        contentAlignment = Alignment.Center
+    ) {
+        Column(
+            horizontalAlignment = Alignment.CenterHorizontally,
+            verticalArrangement = Arrangement.spacedBy(16.dp)
+        ) {
+            Text(
+                text = message,
+                fontSize = 14.sp,
+                color = TextPrimaryLight
+            )
+            Box(
+                modifier = Modifier
+                    .clip(RoundedCornerShape(12.dp))
+                    .background(LovePink)
+                    .clickable(onClick = onRetry)
+                    .padding(horizontal = 24.dp, vertical = 12.dp)
+            ) {
+                Text(
+                    text = "重试",
+                    fontSize = 14.sp,
+                    fontWeight = FontWeight.SemiBold,
+                    color = SurfaceLight
+                )
+            }
+        }
+    }
+}
+
+fun calculateRemainingDays(dateStr: String, repeatType: RepeatType): Int? {
+    return try {
+        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
+        val anniversaryDate = LocalDate.parse(dateStr, formatter)
+        val today = LocalDate.now()
+
+        val nextOccurrence = when (repeatType) {
+            RepeatType.NONE -> anniversaryDate
+            RepeatType.YEARLY -> {
+                var next = anniversaryDate.withYear(today.year)
+                if (next.isBefore(today) || next.isEqual(today)) {
+                    next = next.plusYears(1)
+                }
+                next
+            }
+            RepeatType.MONTHLY -> {
+                var next = anniversaryDate.withYear(today.year).withMonth(today.monthValue)
+                if (next.isBefore(today) || next.isEqual(today)) {
+                    next = next.plusMonths(1)
+                }
+                next
+            }
+        }
+
+        ChronoUnit.DAYS.between(today, nextOccurrence).toInt()
+    } catch (_: Exception) {
+        null
+    }
+}
+
+@Preview(showBackground = true)
+@Composable
+private fun AnniversaryListContentPreview() {
+    LianjiTheme {
+        AnniversaryListContent(
+            uiState = AnniversaryListUiState.Success(
+                anniversaries = listOf(
+                    Anniversary(
+                        id = 1,
+                        coupleId = 1,
+                        title = "恋爱开始日",
+                        date = "2024-01-01",
+                        repeatType = RepeatType.YEARLY,
+                        remindDays = null,
+                        isSystem = true,
+                        createdBy = null
+                    ),
+                    Anniversary(
+                        id = 2,
+                        coupleId = 1,
+                        title = "第一次旅行",
+                        date = "2024-05-20",
+                        repeatType = RepeatType.YEARLY,
+                        remindDays = 7,
+                        isSystem = false,
+                        createdBy = 1
+                    )
+                ),
+                filter = RepeatTypeFilter.ALL
+            ),
+            onEvent = {}
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListScreen.kt
new file mode 100644
index 0000000..2091c47
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListScreen.kt
@@ -0,0 +1,35 @@
+package cn.iven.app.feature.anniversary.ui.list
+
+import androidx.compose.runtime.Composable
+import androidx.compose.runtime.LaunchedEffect
+import androidx.compose.runtime.getValue
+import androidx.compose.ui.Modifier
+import androidx.hilt.navigation.compose.hiltViewModel
+import androidx.lifecycle.compose.collectAsStateWithLifecycle
+
+@Composable
+fun AnniversaryListScreen(
+    onNavigateToCreate: () -> Unit,
+    onNavigateToEdit: (Long) -> Unit,
+    modifier: Modifier = Modifier,
+    viewModel: AnniversaryListViewModel = hiltViewModel()
+) {
+    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
+
+    // Refresh data when screen becomes visible
+    LaunchedEffect(Unit) {
+        viewModel.onEvent(AnniversaryListUiEvent.Refresh)
+    }
+
+    AnniversaryListContent(
+        modifier = modifier,
+        uiState = uiState,
+        onEvent = { event ->
+            when (event) {
+                is AnniversaryListUiEvent.CreateClick -> onNavigateToCreate()
+                is AnniversaryListUiEvent.EditClick -> onNavigateToEdit(event.id)
+                else -> viewModel.onEvent(event)
+            }
+        }
+    )
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiEvent.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiEvent.kt
new file mode 100644
index 0000000..06c42ef
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiEvent.kt
@@ -0,0 +1,10 @@
+package cn.iven.app.feature.anniversary.ui.list
+
+sealed interface AnniversaryListUiEvent {
+    data object Load : AnniversaryListUiEvent
+    data object Refresh : AnniversaryListUiEvent
+    data object CreateClick : AnniversaryListUiEvent
+    data class DeleteClick(val id: Long) : AnniversaryListUiEvent
+    data class EditClick(val id: Long) : AnniversaryListUiEvent
+    data class FilterChanged(val filter: RepeatTypeFilter) : AnniversaryListUiEvent
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiState.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiState.kt
new file mode 100644
index 0000000..8d93c9c
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListUiState.kt
@@ -0,0 +1,17 @@
+package cn.iven.app.feature.anniversary.ui.list
+
+import cn.iven.app.feature.anniversary.domain.Anniversary
+
+sealed interface AnniversaryListUiState {
+    data object Loading : AnniversaryListUiState
+    data class Success(val anniversaries: List<Anniversary>, val filter: RepeatTypeFilter) : AnniversaryListUiState
+    data object Empty : AnniversaryListUiState
+    data class Error(val message: String) : AnniversaryListUiState
+}
+
+enum class RepeatTypeFilter(val label: String) {
+    ALL("全部"),
+    YEARLY("每年"),
+    MONTHLY("每月"),
+    NONE("一次性")
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListViewModel.kt
new file mode 100644
index 0000000..806eec5
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/anniversary/ui/list/AnniversaryListViewModel.kt
@@ -0,0 +1,82 @@
+package cn.iven.app.feature.anniversary.ui.list
+
+import androidx.lifecycle.ViewModel
+import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.anniversary.domain.DeleteAnniversaryUseCase
+import cn.iven.app.feature.anniversary.domain.GetAnniversariesUseCase
+import dagger.hilt.android.lifecycle.HiltViewModel
+import kotlinx.coroutines.flow.MutableStateFlow
+import kotlinx.coroutines.flow.StateFlow
+import kotlinx.coroutines.flow.asStateFlow
+import kotlinx.coroutines.flow.update
+import kotlinx.coroutines.launch
+import javax.inject.Inject
+
+@HiltViewModel
+class AnniversaryListViewModel @Inject constructor(
+    private val getAnniversariesUseCase: GetAnniversariesUseCase,
+    private val deleteAnniversaryUseCase: DeleteAnniversaryUseCase
+) : ViewModel() {
+
+    private val _uiState = MutableStateFlow<AnniversaryListUiState>(AnniversaryListUiState.Loading)
+    val uiState: StateFlow<AnniversaryListUiState> = _uiState.asStateFlow()
+
+    private var allAnniversaries = listOf<cn.iven.app.feature.anniversary.domain.Anniversary>()
+
+    init {
+        loadAnniversaries()
+    }
+
+    fun onEvent(event: AnniversaryListUiEvent) {
+        when (event) {
+            is AnniversaryListUiEvent.Load -> loadAnniversaries()
+            is AnniversaryListUiEvent.Refresh -> loadAnniversaries()
+            is AnniversaryListUiEvent.CreateClick -> { /* navigation handled by screen */ }
+            is AnniversaryListUiEvent.DeleteClick -> deleteAnniversary(event.id)
+            is AnniversaryListUiEvent.EditClick -> { /* navigation handled by screen */ }
+            is AnniversaryListUiEvent.FilterChanged -> applyFilter(event.filter)
+        }
+    }
+
+    private fun loadAnniversaries() {
+        viewModelScope.launch {
+            _uiState.value = AnniversaryListUiState.Loading
+            val result = getAnniversariesUseCase()
+            if (result.isSuccess) {
+                allAnniversaries = result.getOrThrow()
+                val currentFilter = when (val state = _uiState.value) {
+                    is AnniversaryListUiState.Success -> state.filter
+                    else -> RepeatTypeFilter.ALL
+                }
+                applyFilter(currentFilter)
+            } else {
+                _uiState.value = AnniversaryListUiState.Error(
+                    result.exceptionOrNull()?.message ?: "加载失败"
+                )
+            }
+        }
+    }
+
+    private fun applyFilter(filter: RepeatTypeFilter) {
+        val filtered = when (filter) {
+            RepeatTypeFilter.ALL -> allAnniversaries
+            RepeatTypeFilter.YEARLY -> allAnniversaries.filter { it.repeatType == cn.iven.app.feature.anniversary.domain.RepeatType.YEARLY }
+            RepeatTypeFilter.MONTHLY -> allAnniversaries.filter { it.repeatType == cn.iven.app.feature.anniversary.domain.RepeatType.MONTHLY }
+            RepeatTypeFilter.NONE -> allAnniversaries.filter { it.repeatType == cn.iven.app.feature.anniversary.domain.RepeatType.NONE }
+        }
+        _uiState.value = if (filtered.isEmpty() && allAnniversaries.isEmpty()) {
+            AnniversaryListUiState.Empty
+        } else {
+            AnniversaryListUiState.Success(filtered, filter)
+        }
+    }
+
+    private fun deleteAnniversary(id: Long) {
+        viewModelScope.launch {
+            val result = deleteAnniversaryUseCase(id)
+            if (result.isSuccess) {
+                loadAnniversaries()
+            }
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/data/remote/CoupleApi.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/data/remote/CoupleApi.kt
index 9950b12..147b690 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/data/remote/CoupleApi.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/data/remote/CoupleApi.kt
@@ -8,7 +8,9 @@ package cn.iven.app.feature.auth.data.remote
 import cn.iven.app.core.network.ApiResponse
 import kotlinx.serialization.Serializable
 import retrofit2.http.Body
+import retrofit2.http.GET
 import retrofit2.http.POST
+import retrofit2.http.PUT
 
 interface CoupleApi {
 
@@ -19,6 +21,14 @@ interface CoupleApi {
     /** 使用绑定码确认情侣关系 */
     @POST("api/v1/couple/bind")
     suspend fun bind(@Body request: BindRequest): ApiResponse<CoupleResponse>
+
+    /** 更新恋爱开始日期 */
+    @PUT("api/v1/couple/start-date")
+    suspend fun updateStartDate(@Body request: UpdateStartDateRequestDto): ApiResponse<CoupleDto>
+
+    /** 获取当前用户的情侣关系状态 */
+    @GET("api/v1/couple/status")
+    suspend fun getStatus(): ApiResponse<CoupleDto>
 }
 
 /** 绑定码响应 */
@@ -40,3 +50,18 @@ data class CoupleResponse(
     val userAId: Long,
     val userBId: Long
 )
+
+/** 更新恋爱开始日期请求 */
+@Serializable
+data class UpdateStartDateRequestDto(
+    val date: String
+)
+
+/** 情侣信息 DTO */
+@Serializable
+data class CoupleDto(
+    val id: Long,
+    val userAId: Long,
+    val userBId: Long,
+    val startDate: String? = null
+)
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/domain/GetCoupleStatusUseCase.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/domain/GetCoupleStatusUseCase.kt
new file mode 100644
index 0000000..d376bbf
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/domain/GetCoupleStatusUseCase.kt
@@ -0,0 +1,32 @@
+/**
+ * 获取当前用户情侣关系状态用例
+ *
+ * 用于登录后判断用户是否已完成情侣绑定。
+ */
+package cn.iven.app.feature.auth.domain
+
+import cn.iven.app.feature.auth.data.remote.CoupleApi
+import javax.inject.Inject
+
+class GetCoupleStatusUseCase @Inject constructor(
+    private val coupleApi: CoupleApi
+) {
+
+    /**
+     * 查询当前用户是否已有情侣绑定
+     *
+     * @return 成功时返回 Boolean（true=已绑定，false=未绑定），失败时返回异常
+     */
+    suspend operator fun invoke(): Result<Boolean> {
+        return try {
+            val response = coupleApi.getStatus()
+            if (response.isSuccess) {
+                Result.success(response.data != null)
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindScreen.kt
index 25096df..94c6b59 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindScreen.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindScreen.kt
@@ -5,39 +5,45 @@
  */
 package cn.iven.app.feature.auth.ui.bind
 
+import androidx.compose.material3.ExperimentalMaterial3Api
 import androidx.compose.runtime.Composable
-import androidx.compose.runtime.LaunchedEffect
 import androidx.compose.runtime.getValue
 import androidx.hilt.navigation.compose.hiltViewModel
 import androidx.lifecycle.compose.collectAsStateWithLifecycle
 
 /**
  * @param onNavigateBack 返回上一页的回调
- * @param onBindSuccess 绑定成功后的回调（通常用于导航到主页）
- * @param onSkip 跳过绑定的回调
+ * @param onBindComplete 绑定流程完成后的回调（包括设置/跳过开始日期）
  * @param viewModel 绑定 ViewModel，由 Hilt 注入
  */
+@OptIn(ExperimentalMaterial3Api::class)
 @Composable
 fun BindScreen(
     onNavigateBack: () -> Unit,
-    onBindSuccess: () -> Unit,
-    onSkip: () -> Unit,
+    onBindComplete: () -> Unit,
     viewModel: BindViewModel = hiltViewModel()
 ) {
     val uiState by viewModel.uiState.collectAsStateWithLifecycle()
     val codeInput by viewModel.codeInput.collectAsStateWithLifecycle()
-
-    LaunchedEffect(uiState) {
-        if (uiState is BindUiState.Bound) {
-            onBindSuccess()
-        }
-    }
+    val showStartDateSheet by viewModel.showStartDateSheet.collectAsStateWithLifecycle()
+    val startDateSubmitState by viewModel.startDateSubmitState.collectAsStateWithLifecycle()
 
     BindContent(
         uiState = uiState,
         codeInput = codeInput,
         onEvent = viewModel::onEvent,
         onNavigateBack = onNavigateBack,
-        onSkip = onSkip
+        onSkip = { viewModel.skipStartDate(onBindComplete) }
     )
+
+    if (showStartDateSheet) {
+        StartDateBottomSheet(
+            onDismiss = { viewModel.dismissStartDateSheet() },
+            onConfirm = { date ->
+                viewModel.submitStartDate(date) { onBindComplete() }
+            },
+            onSkip = { viewModel.skipStartDate(onBindComplete) },
+            isLoading = startDateSubmitState is StartDateSubmitState.Loading
+        )
+    }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindViewModel.kt
index 96581ad..9ea0c8a 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindViewModel.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/BindViewModel.kt
@@ -7,6 +7,7 @@ package cn.iven.app.feature.auth.ui.bind
 
 import androidx.lifecycle.ViewModel
 import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.anniversary.domain.UpdateCoupleStartDateUseCase
 import cn.iven.app.feature.auth.domain.BindCoupleUseCase
 import cn.iven.app.feature.auth.domain.GenerateBindingCodeUseCase
 import dagger.hilt.android.lifecycle.HiltViewModel
@@ -20,7 +21,8 @@ import javax.inject.Inject
 @HiltViewModel
 class BindViewModel @Inject constructor(
     private val generateBindingCodeUseCase: GenerateBindingCodeUseCase,
-    private val bindCoupleUseCase: BindCoupleUseCase
+    private val bindCoupleUseCase: BindCoupleUseCase,
+    private val updateCoupleStartDateUseCase: UpdateCoupleStartDateUseCase
 ) : ViewModel() {
 
     private val _uiState = MutableStateFlow<BindUiState>(BindUiState.Idle)
@@ -33,6 +35,16 @@ class BindViewModel @Inject constructor(
     /** 用户输入的绑定码 */
     val codeInput: StateFlow<String> = _codeInput.asStateFlow()
 
+    private val _showStartDateSheet = MutableStateFlow(false)
+
+    /** 是否显示开始日期设置 BottomSheet */
+    val showStartDateSheet: StateFlow<Boolean> = _showStartDateSheet.asStateFlow()
+
+    private val _startDateSubmitState = MutableStateFlow<StartDateSubmitState>(StartDateSubmitState.Idle)
+
+    /** 开始日期提交状态 */
+    val startDateSubmitState: StateFlow<StartDateSubmitState> = _startDateSubmitState.asStateFlow()
+
     /** 处理 UI 事件 */
     fun onEvent(event: BindUiEvent) {
         when (event) {
@@ -66,11 +78,48 @@ class BindViewModel @Inject constructor(
         viewModelScope.launch {
             _uiState.value = BindUiState.Binding
             val result = bindCoupleUseCase(code)
-            _uiState.value = if (result.isSuccess) {
-                BindUiState.Bound
+            if (result.isSuccess) {
+                _uiState.value = BindUiState.Bound
+                _showStartDateSheet.value = true
+            } else {
+                _uiState.value = BindUiState.Error(result.exceptionOrNull()?.message ?: "绑定失败")
+            }
+        }
+    }
+
+    /** 提交恋爱开始日期 */
+    fun submitStartDate(date: String, onSuccess: () -> Unit) {
+        viewModelScope.launch {
+            _startDateSubmitState.value = StartDateSubmitState.Loading
+            val result = updateCoupleStartDateUseCase(date)
+            _startDateSubmitState.value = if (result.isSuccess) {
+                StartDateSubmitState.Success
             } else {
-                BindUiState.Error(result.exceptionOrNull()?.message ?: "绑定失败")
+                StartDateSubmitState.Error(result.exceptionOrNull()?.message ?: "设置失败")
+            }
+            if (result.isSuccess) {
+                _showStartDateSheet.value = false
+                onSuccess()
             }
         }
     }
+
+    /** 跳过设置开始日期 */
+    fun skipStartDate(onSuccess: () -> Unit) {
+        _showStartDateSheet.value = false
+        onSuccess()
+    }
+
+    /** 关闭 BottomSheet */
+    fun dismissStartDateSheet() {
+        _showStartDateSheet.value = false
+    }
+}
+
+/** 开始日期提交状态 */
+sealed interface StartDateSubmitState {
+    data object Idle : StartDateSubmitState
+    data object Loading : StartDateSubmitState
+    data object Success : StartDateSubmitState
+    data class Error(val message: String) : StartDateSubmitState
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/StartDateBottomSheet.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/StartDateBottomSheet.kt
new file mode 100644
index 0000000..df0a642
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/bind/StartDateBottomSheet.kt
@@ -0,0 +1,231 @@
+package cn.iven.app.feature.auth.ui.bind
+
+import android.app.DatePickerDialog
+import androidx.compose.foundation.background
+import androidx.compose.foundation.clickable
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.height
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
+import androidx.compose.foundation.shape.CircleShape
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.filled.CalendarToday
+import androidx.compose.material.icons.filled.Favorite
+import androidx.compose.material3.CircularProgressIndicator
+import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.Icon
+import androidx.compose.material3.MaterialTheme
+import androidx.compose.material3.ModalBottomSheet
+import androidx.compose.material3.SheetState
+import androidx.compose.material3.Text
+import androidx.compose.material3.rememberModalBottomSheetState
+import androidx.compose.runtime.Composable
+import androidx.compose.runtime.getValue
+import androidx.compose.runtime.mutableStateOf
+import androidx.compose.runtime.remember
+import androidx.compose.runtime.setValue
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.platform.LocalContext
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.tooling.preview.Preview
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.ui.theme.BackgroundLight
+import cn.iven.app.ui.theme.DividerLight
+import cn.iven.app.ui.theme.LianjiTheme
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import cn.iven.app.ui.theme.TextSecondaryLight
+import java.time.LocalDate
+import java.time.format.DateTimeFormatter
+import java.time.temporal.ChronoUnit
+import java.util.Calendar
+
+@OptIn(ExperimentalMaterial3Api::class)
+@Composable
+fun StartDateBottomSheet(
+    onDismiss: () -> Unit,
+    onConfirm: (String) -> Unit,
+    onSkip: () -> Unit,
+    isLoading: Boolean = false,
+    sheetState: SheetState = rememberModalBottomSheetState(skipPartiallyExpanded = true)
+) {
+    val context = LocalContext.current
+    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
+    var selectedDate by remember { mutableStateOf(LocalDate.now().format(formatter)) }
+
+    val daysCount = remember(selectedDate) {
+        try {
+            val date = LocalDate.parse(selectedDate, formatter)
+            val today = LocalDate.now()
+            ChronoUnit.DAYS.between(date, today).coerceAtLeast(0).toInt()
+        } catch (_: Exception) {
+            0
+        }
+    }
+
+    val datePickerDialog = DatePickerDialog(
+        context,
+        { _, year, month, dayOfMonth ->
+            selectedDate = LocalDate.of(year, month + 1, dayOfMonth).format(formatter)
+        },
+        Calendar.getInstance().get(Calendar.YEAR),
+        Calendar.getInstance().get(Calendar.MONTH),
+        Calendar.getInstance().get(Calendar.DAY_OF_MONTH)
+    )
+
+    // Pre-select current date
+    try {
+        val date = LocalDate.parse(selectedDate, formatter)
+        datePickerDialog.datePicker.updateDate(date.year, date.monthValue - 1, date.dayOfMonth)
+    } catch (_: Exception) { }
+
+    ModalBottomSheet(
+        onDismissRequest = onDismiss,
+        sheetState = sheetState,
+        containerColor = SurfaceLight,
+        shape = RoundedCornerShape(topStart = 24.dp, topEnd = 24.dp)
+    ) {
+        Column(
+            modifier = Modifier
+                .fillMaxWidth()
+                .padding(horizontal = 24.dp)
+                .padding(bottom = 32.dp),
+            horizontalAlignment = Alignment.CenterHorizontally,
+            verticalArrangement = Arrangement.spacedBy(20.dp)
+        ) {
+            // Heart icon
+            Box(
+                modifier = Modifier
+                    .size(80.dp)
+                    .clip(CircleShape)
+                    .background(LovePinkLight),
+                contentAlignment = Alignment.Center
+            ) {
+                Icon(
+                    imageVector = Icons.Default.Favorite,
+                    contentDescription = null,
+                    modifier = Modifier.size(40.dp),
+                    tint = LovePink
+                )
+            }
+
+            // Title
+            Text(
+                text = "设置恋爱开始日期",
+                fontSize = 20.sp,
+                fontWeight = FontWeight.Bold,
+                color = TextPrimaryLight
+            )
+
+            Text(
+                text = "选择你们在一起的第一天",
+                fontSize = 14.sp,
+                color = TextSecondaryLight
+            )
+
+            // Date selector
+            Row(
+                modifier = Modifier
+                    .fillMaxWidth()
+                    .height(56.dp)
+                    .clip(RoundedCornerShape(14.dp))
+                    .background(BackgroundLight)
+                    .clickable { datePickerDialog.show() }
+                    .padding(horizontal = 20.dp),
+                verticalAlignment = Alignment.CenterVertically,
+                horizontalArrangement = Arrangement.SpaceBetween
+            ) {
+                Text(
+                    text = selectedDate,
+                    fontSize = 16.sp,
+                    fontWeight = FontWeight.Medium,
+                    color = TextPrimaryLight
+                )
+                Icon(
+                    imageVector = Icons.Default.CalendarToday,
+                    contentDescription = null,
+                    modifier = Modifier.size(22.dp),
+                    tint = LovePink
+                )
+            }
+
+            // Days counter preview
+            Box(
+                modifier = Modifier
+                    .fillMaxWidth()
+                    .clip(RoundedCornerShape(14.dp))
+                    .background(LovePinkLight)
+                    .padding(vertical = 16.dp),
+                contentAlignment = Alignment.Center
+            ) {
+                Text(
+                    text = "已相爱 ${daysCount} 天",
+                    fontSize = 18.sp,
+                    fontWeight = FontWeight.SemiBold,
+                    color = LovePink
+                )
+            }
+
+            Spacer(modifier = Modifier.height(8.dp))
+
+            // Confirm button
+            Box(
+                modifier = Modifier
+                    .fillMaxWidth()
+                    .height(52.dp)
+                    .clip(RoundedCornerShape(14.dp))
+                    .background(LovePink)
+                    .clickable(enabled = !isLoading) { onConfirm(selectedDate) },
+                contentAlignment = Alignment.Center
+            ) {
+                if (isLoading) {
+                    CircularProgressIndicator(
+                        modifier = Modifier.size(24.dp),
+                        color = SurfaceLight,
+                        strokeWidth = 2.dp
+                    )
+                } else {
+                    Text(
+                        text = "完成绑定",
+                        fontSize = 16.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = SurfaceLight
+                    )
+                }
+            }
+
+            // Skip text
+            Text(
+                text = "跳过",
+                fontSize = 14.sp,
+                fontWeight = FontWeight.Medium,
+                color = TextSecondaryLight,
+                modifier = Modifier.clickable(enabled = !isLoading) { onSkip() }
+            )
+        }
+    }
+}
+
+@OptIn(ExperimentalMaterial3Api::class)
+@Preview(showBackground = true)
+@Composable
+private fun StartDateBottomSheetPreview() {
+    LianjiTheme {
+        StartDateBottomSheet(
+            onDismiss = {},
+            onConfirm = {},
+            onSkip = {}
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginScreen.kt
index b084f6b..f072ea1 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginScreen.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginScreen.kt
@@ -19,15 +19,16 @@ import androidx.lifecycle.compose.collectAsStateWithLifecycle
 @Composable
 fun LoginScreen(
     onNavigateToRegister: () -> Unit,
-    onLoginSuccess: () -> Unit,
+    onLoginSuccess: (hasCouple: Boolean) -> Unit,
     viewModel: LoginViewModel = hiltViewModel()
 ) {
     val formState by viewModel.formState.collectAsStateWithLifecycle()
     val submitState by viewModel.submitState.collectAsStateWithLifecycle()
 
     LaunchedEffect(submitState) {
-        if (submitState is LoginSubmitState.Success) {
-            onLoginSuccess()
+        val state = submitState
+        if (state is LoginSubmitState.Success) {
+            onLoginSuccess(state.hasCouple)
         }
     }
 
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginUiState.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginUiState.kt
index dc1819f..030a060 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginUiState.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginUiState.kt
@@ -11,8 +11,8 @@ sealed interface LoginSubmitState {
     data object Idle : LoginSubmitState
     /** 提交中 */
     data object Loading : LoginSubmitState
-    /** 提交成功 */
-    data object Success : LoginSubmitState
+    /** 提交成功，携带是否已有情侣绑定 */
+    data class Success(val hasCouple: Boolean) : LoginSubmitState
     /** 提交失败，携带错误信息 */
     data class Error(val message: String) : LoginSubmitState
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginViewModel.kt
index 861ad30..e6cd68c 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginViewModel.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/auth/ui/login/LoginViewModel.kt
@@ -7,6 +7,7 @@ package cn.iven.app.feature.auth.ui.login
 
 import androidx.lifecycle.ViewModel
 import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.auth.domain.GetCoupleStatusUseCase
 import cn.iven.app.feature.auth.domain.LoginUseCase
 import dagger.hilt.android.lifecycle.HiltViewModel
 import kotlinx.coroutines.flow.MutableStateFlow
@@ -18,7 +19,8 @@ import javax.inject.Inject
 
 @HiltViewModel
 class LoginViewModel @Inject constructor(
-    private val loginUseCase: LoginUseCase
+    private val loginUseCase: LoginUseCase,
+    private val getCoupleStatusUseCase: GetCoupleStatusUseCase
 ) : ViewModel() {
 
     private val _formState = MutableStateFlow(LoginFormState())
@@ -57,11 +59,13 @@ class LoginViewModel @Inject constructor(
 
         viewModelScope.launch {
             _submitState.value = LoginSubmitState.Loading
-            val result = loginUseCase(form.email, form.password)
-            _submitState.value = if (result.isSuccess) {
-                LoginSubmitState.Success
+            val loginResult = loginUseCase(form.email, form.password)
+            if (loginResult.isSuccess) {
+                val statusResult = getCoupleStatusUseCase()
+                val hasCouple = statusResult.isSuccess && statusResult.getOrDefault(false)
+                _submitState.value = LoginSubmitState.Success(hasCouple)
             } else {
-                LoginSubmitState.Error(result.exceptionOrNull()?.message ?: "登录失败")
+                _submitState.value = LoginSubmitState.Error(loginResult.exceptionOrNull()?.message ?: "登录失败")
             }
         }
     }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
index 00ad6ca..5b5b78f 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
@@ -57,6 +57,7 @@ import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
 @Composable
 fun HomeScreen(
     modifier: Modifier = Modifier,
+    onNavigateToAnniversary: () -> Unit = {},
     viewModel: HomeViewModel = hiltViewModel()
 ) {
     val uiState by viewModel.uiState.collectAsStateWithLifecycle()
@@ -121,7 +122,8 @@ fun HomeScreen(
                     HomeContent(
                         statsCards = state.statsCards,
                         upcomingAnniversary = state.upcomingAnniversary,
-                        recentMemories = state.recentMemories
+                        recentMemories = state.recentMemories,
+                        onNavigateToAnniversary = onNavigateToAnniversary
                     )
                 }
             }
@@ -134,6 +136,7 @@ private fun HomeContent(
     statsCards: List<StatsCard>,
     upcomingAnniversary: AnniversaryCard?,
     recentMemories: List<MemoryTimelineItem>,
+    onNavigateToAnniversary: () -> Unit = {},
     modifier: Modifier = Modifier
 ) {
     Column(
@@ -145,7 +148,10 @@ private fun HomeContent(
         verticalArrangement = Arrangement.spacedBy(24.dp)
     ) {
         StatsCardsSection(statsCards = statsCards)
-        UpcomingAnniversarySection(anniversary = upcomingAnniversary)
+        UpcomingAnniversarySection(
+            anniversary = upcomingAnniversary,
+            onViewAllClick = onNavigateToAnniversary
+        )
         RecentMemoriesSection(memories = recentMemories)
     }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt
index e19ff1f..b587050 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt
@@ -7,6 +7,7 @@ package cn.iven.app.feature.home.ui
 
 import androidx.lifecycle.ViewModel
 import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.anniversary.domain.GetUpcomingAnniversariesUseCase
 import cn.iven.app.feature.home.domain.HomeRepository
 import dagger.hilt.android.lifecycle.HiltViewModel
 import kotlinx.coroutines.flow.MutableStateFlow
@@ -17,7 +18,8 @@ import javax.inject.Inject
 
 @HiltViewModel
 class HomeViewModel @Inject constructor(
-    private val repository: HomeRepository
+    private val repository: HomeRepository,
+    private val getUpcomingAnniversariesUseCase: GetUpcomingAnniversariesUseCase
 ) : ViewModel() {
 
     private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
@@ -41,16 +43,27 @@ class HomeViewModel @Inject constructor(
     private fun loadStats() {
         viewModelScope.launch {
             _uiState.value = HomeUiState.Loading
-            val result = repository.getHomeStats()
-            _uiState.value = if (result.isSuccess) {
-                val stats = result.getOrThrow()
-                HomeUiState.Success(
+            val statsResult = repository.getHomeStats()
+            val upcomingResult = getUpcomingAnniversariesUseCase(limit = 1)
+
+            if (statsResult.isSuccess) {
+                val stats = statsResult.getOrThrow()
+                val upcoming = if (upcomingResult.isSuccess) {
+                    upcomingResult.getOrThrow().firstOrNull()
+                } else null
+
+                _uiState.value = HomeUiState.Success(
                     statsCards = stats.statsCards,
-                    upcomingAnniversary = stats.upcomingAnniversary,
+                    upcomingAnniversary = upcoming?.let {
+                        cn.iven.app.feature.home.domain.model.AnniversaryCard(
+                            title = it.title,
+                            remainingDays = it.remainingDays
+                        )
+                    },
                     recentMemories = stats.recentMemories
                 )
             } else {
-                HomeUiState.Error(result.exceptionOrNull()?.message ?: "加载失败")
+                _uiState.value = HomeUiState.Error(statsResult.exceptionOrNull()?.message ?: "加载失败")
             }
         }
     }
@@ -58,16 +71,27 @@ class HomeViewModel @Inject constructor(
     /** 刷新首页数据（用于下拉刷新） */
     private fun refresh() {
         viewModelScope.launch {
-            val result = repository.getHomeStats()
-            _uiState.value = if (result.isSuccess) {
-                val stats = result.getOrThrow()
-                HomeUiState.Success(
+            val statsResult = repository.getHomeStats()
+            val upcomingResult = getUpcomingAnniversariesUseCase(limit = 1)
+
+            if (statsResult.isSuccess) {
+                val stats = statsResult.getOrThrow()
+                val upcoming = if (upcomingResult.isSuccess) {
+                    upcomingResult.getOrThrow().firstOrNull()
+                } else null
+
+                _uiState.value = HomeUiState.Success(
                     statsCards = stats.statsCards,
-                    upcomingAnniversary = stats.upcomingAnniversary,
+                    upcomingAnniversary = upcoming?.let {
+                        cn.iven.app.feature.home.domain.model.AnniversaryCard(
+                            title = it.title,
+                            remainingDays = it.remainingDays
+                        )
+                    },
                     recentMemories = stats.recentMemories
                 )
             } else {
-                HomeUiState.Error(result.exceptionOrNull()?.message ?: "刷新失败")
+                _uiState.value = HomeUiState.Error(statsResult.exceptionOrNull()?.message ?: "刷新失败")
             }
         }
     }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt
index f50df46..4fc39b3 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt
@@ -6,6 +6,7 @@
 package cn.iven.app.feature.home.ui.components
 
 import androidx.compose.foundation.background
+import androidx.compose.foundation.clickable
 import androidx.compose.foundation.layout.Arrangement
 import androidx.compose.foundation.layout.Box
 import androidx.compose.foundation.layout.Column
@@ -41,13 +42,14 @@ import cn.iven.app.ui.theme.WarmOrange
 @Composable
 fun UpcomingAnniversarySection(
     anniversary: AnniversaryCard?,
+    onViewAllClick: () -> Unit = {},
     modifier: Modifier = Modifier
 ) {
     Column(
         modifier = modifier.fillMaxWidth(),
         verticalArrangement = Arrangement.spacedBy(12.dp)
     ) {
-        // 标题行
+        // Title row
         Row(
             modifier = Modifier.fillMaxWidth(),
             horizontalArrangement = Arrangement.SpaceBetween,
@@ -63,13 +65,16 @@ fun UpcomingAnniversarySection(
                 text = "查看全部",
                 fontSize = 13.sp,
                 fontWeight = FontWeight.Medium,
-                color = LovePink
+                color = LovePink,
+                modifier = Modifier.clickable { onViewAllClick() }
             )
         }
 
-        // 纪念日卡片
+        // Anniversary card
         if (anniversary != null) {
             AnniversaryCardItem(anniversary = anniversary)
+        } else {
+            EmptyAnniversaryCard()
         }
     }
 }
@@ -90,7 +95,7 @@ private fun AnniversaryCardItem(
                 .padding(16.dp),
             verticalAlignment = Alignment.CenterVertically
         ) {
-            // 蛋糕图标
+            // Cake icon
             Box(
                 modifier = Modifier
                     .size(40.dp)
@@ -108,7 +113,7 @@ private fun AnniversaryCardItem(
 
             Spacer(modifier = Modifier.width(12.dp))
 
-            // 标题和天数
+            // Title and days
             Column(
                 verticalArrangement = Arrangement.spacedBy(2.dp)
             ) {
@@ -128,3 +133,45 @@ private fun AnniversaryCardItem(
         }
     }
 }
+
+@Composable
+private fun EmptyAnniversaryCard(
+    modifier: Modifier = Modifier
+) {
+    Card(
+        modifier = modifier.fillMaxWidth(),
+        colors = CardDefaults.cardColors(containerColor = SurfaceLight),
+        shape = RoundedCornerShape(12.dp)
+    ) {
+        Row(
+            modifier = Modifier
+                .fillMaxWidth()
+                .padding(16.dp),
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            Box(
+                modifier = Modifier
+                    .size(40.dp)
+                    .clip(CircleShape)
+                    .background(LovePinkLight),
+                contentAlignment = Alignment.Center
+            ) {
+                Icon(
+                    imageVector = Icons.Default.Cake,
+                    contentDescription = null,
+                    modifier = Modifier.size(20.dp),
+                    tint = LovePink
+                )
+            }
+
+            Spacer(modifier = Modifier.width(12.dp))
+
+            Text(
+                text = "暂无即将到来的纪念日",
+                fontSize = 14.sp,
+                fontWeight = FontWeight.Medium,
+                color = TextSecondaryLight
+            )
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt
index 788182f..c1c3f7f 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt
@@ -1,37 +1,98 @@
 package cn.iven.app.feature.profile.ui
 
+import android.app.DatePickerDialog
+import android.widget.Toast
+import androidx.compose.foundation.background
+import androidx.compose.foundation.clickable
+import androidx.compose.foundation.layout.Arrangement
 import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
 import androidx.compose.foundation.layout.fillMaxSize
 import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.height
 import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
 import androidx.compose.foundation.shape.RoundedCornerShape
-import androidx.compose.material3.Button
-import androidx.compose.material3.ButtonDefaults
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
+import androidx.compose.material.icons.filled.Favorite
+import androidx.compose.material3.CircularProgressIndicator
 import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.Icon
 import androidx.compose.material3.Scaffold
 import androidx.compose.material3.Text
 import androidx.compose.material3.TopAppBar
 import androidx.compose.material3.TopAppBarDefaults
 import androidx.compose.runtime.Composable
+import androidx.compose.runtime.getValue
+import androidx.compose.runtime.mutableStateOf
+import androidx.compose.runtime.remember
+import androidx.compose.runtime.setValue
 import androidx.compose.ui.Alignment
 import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.platform.LocalContext
 import androidx.compose.ui.text.font.FontWeight
 import androidx.compose.ui.unit.dp
 import androidx.compose.ui.unit.sp
 import androidx.hilt.navigation.compose.hiltViewModel
+import androidx.lifecycle.ViewModel
+import androidx.lifecycle.compose.collectAsStateWithLifecycle
+import androidx.lifecycle.viewModelScope
 import cn.iven.app.core.network.AuthNavigator
+import cn.iven.app.feature.anniversary.domain.UpdateCoupleStartDateUseCase
 import cn.iven.app.ui.theme.BackgroundLight
 import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
 import cn.iven.app.ui.theme.SurfaceLight
 import cn.iven.app.ui.theme.TextPrimaryLight
-import androidx.lifecycle.ViewModel
+import cn.iven.app.ui.theme.TextSecondaryLight
 import dagger.hilt.android.lifecycle.HiltViewModel
+import kotlinx.coroutines.flow.MutableStateFlow
+import kotlinx.coroutines.flow.StateFlow
+import kotlinx.coroutines.flow.asStateFlow
+import kotlinx.coroutines.launch
+import java.time.LocalDate
+import java.time.format.DateTimeFormatter
+import java.time.temporal.ChronoUnit
+import java.util.Calendar
 import javax.inject.Inject
 
 @HiltViewModel
 class ProfileViewModel @Inject constructor(
-    val authNavigator: AuthNavigator
-) : ViewModel()
+    val authNavigator: AuthNavigator,
+    private val updateCoupleStartDateUseCase: UpdateCoupleStartDateUseCase
+) : ViewModel() {
+
+    private val _updateState = MutableStateFlow<UpdateStartDateState>(UpdateStartDateState.Idle)
+    val updateState: StateFlow<UpdateStartDateState> = _updateState.asStateFlow()
+
+    fun updateStartDate(date: String, onSuccess: () -> Unit) {
+        viewModelScope.launch {
+            _updateState.value = UpdateStartDateState.Loading
+            val result = updateCoupleStartDateUseCase(date)
+            _updateState.value = if (result.isSuccess) {
+                onSuccess()
+                UpdateStartDateState.Success
+            } else {
+                UpdateStartDateState.Error(result.exceptionOrNull()?.message ?: "更新失败")
+            }
+        }
+    }
+
+    fun resetState() {
+        _updateState.value = UpdateStartDateState.Idle
+    }
+}
+
+sealed interface UpdateStartDateState {
+    data object Idle : UpdateStartDateState
+    data object Loading : UpdateStartDateState
+    data object Success : UpdateStartDateState
+    data class Error(val message: String) : UpdateStartDateState
+}
 
 @OptIn(ExperimentalMaterial3Api::class)
 @Composable
@@ -39,6 +100,34 @@ fun ProfileScreen(
     modifier: Modifier = Modifier,
     viewModel: ProfileViewModel = hiltViewModel()
 ) {
+    val context = LocalContext.current
+    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd")
+    var selectedDate by remember { mutableStateOf(LocalDate.now().format(formatter)) }
+    val updateState by viewModel.updateState.collectAsStateWithLifecycle()
+
+    val daysCount = remember(selectedDate) {
+        try {
+            val date = LocalDate.parse(selectedDate, formatter)
+            val today = LocalDate.now()
+            ChronoUnit.DAYS.between(date, today).coerceAtLeast(0).toInt()
+        } catch (_: Exception) {
+            0
+        }
+    }
+
+    val datePickerDialog = DatePickerDialog(
+        context,
+        { _, year, month, dayOfMonth ->
+            selectedDate = LocalDate.of(year, month + 1, dayOfMonth).format(formatter)
+            viewModel.updateStartDate(selectedDate) {
+                Toast.makeText(context, "恋爱开始日期已更新", Toast.LENGTH_SHORT).show()
+            }
+        },
+        Calendar.getInstance().get(Calendar.YEAR),
+        Calendar.getInstance().get(Calendar.MONTH),
+        Calendar.getInstance().get(Calendar.DAY_OF_MONTH)
+    )
+
     Scaffold(
         modifier = modifier,
         topBar = {
@@ -57,27 +146,100 @@ fun ProfileScreen(
             )
         }
     ) { paddingValues ->
-        Box(
+        Column(
             modifier = Modifier
                 .fillMaxSize()
+                .background(BackgroundLight)
                 .padding(paddingValues)
                 .padding(16.dp),
-            contentAlignment = Alignment.BottomCenter
+            verticalArrangement = Arrangement.spacedBy(16.dp)
         ) {
-            Button(
-                onClick = { viewModel.authNavigator.logout() },
-                modifier = Modifier.fillMaxWidth(),
-                shape = RoundedCornerShape(12.dp),
-                colors = ButtonDefaults.buttonColors(
-                    containerColor = LovePink,
-                    contentColor = SurfaceLight
-                )
+            // Start date setting card
+            Box(
+                modifier = Modifier
+                    .fillMaxWidth()
+                    .clip(RoundedCornerShape(16.dp))
+                    .background(SurfaceLight)
+                    .clickable(
+                        enabled = updateState != UpdateStartDateState.Loading
+                    ) { datePickerDialog.show() }
+                    .padding(20.dp)
+            ) {
+                Row(
+                    modifier = Modifier.fillMaxWidth(),
+                    verticalAlignment = Alignment.CenterVertically,
+                    horizontalArrangement = Arrangement.SpaceBetween
+                ) {
+                    Row(
+                        verticalAlignment = Alignment.CenterVertically,
+                        horizontalArrangement = Arrangement.spacedBy(14.dp)
+                    ) {
+                        Box(
+                            modifier = Modifier
+                                .size(44.dp)
+                                .clip(RoundedCornerShape(12.dp))
+                                .background(LovePinkLight),
+                            contentAlignment = Alignment.Center
+                        ) {
+                            Icon(
+                                imageVector = Icons.Default.Favorite,
+                                contentDescription = null,
+                                modifier = Modifier.size(22.dp),
+                                tint = LovePink
+                            )
+                        }
+
+                        Column(
+                            verticalArrangement = Arrangement.spacedBy(4.dp)
+                        ) {
+                            Text(
+                                text = "恋爱开始日期",
+                                fontSize = 15.sp,
+                                fontWeight = FontWeight.Medium,
+                                color = TextPrimaryLight
+                            )
+                            Text(
+                                text = "$selectedDate  ·  已相爱 ${daysCount} 天",
+                                fontSize = 13.sp,
+                                color = TextSecondaryLight
+                            )
+                        }
+                    }
+
+                    if (updateState is UpdateStartDateState.Loading) {
+                        CircularProgressIndicator(
+                            modifier = Modifier.size(20.dp),
+                            color = LovePink,
+                            strokeWidth = 2.dp
+                        )
+                    } else {
+                        Icon(
+                            imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
+                            contentDescription = null,
+                            modifier = Modifier.size(20.dp),
+                            tint = TextSecondaryLight
+                        )
+                    }
+                }
+            }
+
+            Spacer(modifier = Modifier.weight(1f))
+
+            // Logout button
+            Box(
+                modifier = Modifier
+                    .fillMaxWidth()
+                    .height(52.dp)
+                    .clip(RoundedCornerShape(14.dp))
+                    .background(LovePink)
+                    .clickable { viewModel.authNavigator.logout() },
+                contentAlignment = Alignment.Center
             ) {
                 Text(
                     text = "退出登录",
                     fontSize = 16.sp,
                     fontWeight = FontWeight.SemiBold,
-                    modifier = Modifier.padding(vertical = 4.dp)
+                    color = SurfaceLight
                 )
             }
         }
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/AuthNavGraph.kt b/src/app/app/src/main/java/cn/iven/app/navigation/AuthNavGraph.kt
index de2337c..aa3c184 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/AuthNavGraph.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/AuthNavGraph.kt
@@ -2,6 +2,7 @@
  * 认证流程导航图
  *
  * 包含登录、注册、情侣绑定三个页面的路由配置和页面跳转逻辑。
+ * 登录/注册成功后根据用户是否已绑定情侣决定跳转目标。
  */
 package cn.iven.app.navigation
 
@@ -27,9 +28,13 @@ fun NavGraphBuilder.authNavGraph(
                 onNavigateToRegister = {
                     navController.navigate(Routes.REGISTER)
                 },
-                onLoginSuccess = {
-                    navController.navigate(Routes.BIND) {
-                        popUpTo(Routes.LOGIN) { inclusive = true }
+                onLoginSuccess = { hasCouple ->
+                    if (hasCouple) {
+                        onAuthSuccess()
+                    } else {
+                        navController.navigate(Routes.BIND) {
+                            popUpTo(Routes.LOGIN) { inclusive = true }
+                        }
                     }
                 }
             )
@@ -54,8 +59,7 @@ fun NavGraphBuilder.authNavGraph(
                 onNavigateBack = {
                     navController.popBackStack()
                 },
-                onBindSuccess = onAuthSuccess,
-                onSkip = onAuthSuccess
+                onBindComplete = onAuthSuccess
             )
         }
     }
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt b/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
index d552a6d..6700514 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/LianjiNavHost.kt
@@ -2,13 +2,46 @@
  * 应用全局导航宿主
  *
  * 组合认证导航图和主页导航图，根据登录状态决定起始目的地。
+ * Scaffold + BottomBar 在此层统一管理，独立于页面切换。
  */
 package cn.iven.app.navigation
 
+import android.widget.Toast
+import androidx.compose.foundation.layout.padding
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.automirrored.filled.Chat
+import androidx.compose.material.icons.filled.Book
+import androidx.compose.material.icons.filled.CalendarToday
+import androidx.compose.material.icons.filled.Home
+import androidx.compose.material.icons.filled.Person
+import androidx.compose.material3.Icon
+import androidx.compose.material3.NavigationBar
+import androidx.compose.material3.NavigationBarItem
+import androidx.compose.material3.Scaffold
+import androidx.compose.material3.Text
 import androidx.compose.runtime.Composable
+import androidx.compose.runtime.getValue
 import androidx.compose.ui.Modifier
+import androidx.compose.ui.platform.LocalContext
 import androidx.navigation.NavHostController
 import androidx.navigation.compose.NavHost
+import androidx.navigation.compose.currentBackStackEntryAsState
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.TextSecondaryLight
+
+private data class BottomNavItem(
+    val route: String,
+    val label: String,
+    val icon: androidx.compose.ui.graphics.vector.ImageVector
+)
+
+private val bottomNavItems = listOf(
+    BottomNavItem(Routes.HOME, "首页", Icons.Default.Home),
+    BottomNavItem(Routes.NOTE, "记事", Icons.Default.Book),
+    BottomNavItem(Routes.ANNIVERSARY, "纪念日", Icons.Default.CalendarToday),
+    BottomNavItem(Routes.CHAT, "聊天", Icons.AutoMirrored.Filled.Chat),
+    BottomNavItem(Routes.PROFILE, "我的", Icons.Default.Person)
+)
 
 /**
  * @param navController 导航控制器
@@ -23,15 +56,63 @@ fun LianjiNavHost(
     onAuthSuccess: () -> Unit,
     modifier: Modifier = Modifier
 ) {
-    NavHost(
-        navController = navController,
-        startDestination = startDestination,
-        modifier = modifier
-    ) {
-        authNavGraph(
+    val navBackStackEntry by navController.currentBackStackEntryAsState()
+    val currentRoute = navBackStackEntry?.destination?.route
+    val context = LocalContext.current
+
+    val bottomNavRoutes = setOf(Routes.HOME, Routes.NOTE, Routes.ANNIVERSARY, Routes.CHAT, Routes.PROFILE)
+    val showBottomNav = currentRoute in bottomNavRoutes
+
+    Scaffold(
+        bottomBar = {
+            if (showBottomNav) {
+                NavigationBar {
+                    bottomNavItems.forEach { item ->
+                        val selected = currentRoute == item.route
+                        val isImplemented = item.route == Routes.HOME || item.route == Routes.ANNIVERSARY || item.route == Routes.PROFILE
+
+                        NavigationBarItem(
+                            icon = {
+                                Icon(
+                                    imageVector = item.icon,
+                                    contentDescription = item.label,
+                                    tint = if (selected) LovePink else TextSecondaryLight
+                                )
+                            },
+                            label = {
+                                Text(
+                                    text = item.label,
+                                    color = if (selected) LovePink else TextSecondaryLight
+                                )
+                            },
+                            selected = selected,
+                            onClick = {
+                                if (isImplemented) {
+                                    if (currentRoute != item.route) {
+                                        navController.navigate(item.route) {
+                                            popUpTo(Routes.MAIN) { inclusive = false }
+                                        }
+                                    }
+                                } else {
+                                    Toast.makeText(context, "功能开发中", Toast.LENGTH_SHORT).show()
+                                }
+                            }
+                        )
+                    }
+                }
+            }
+        }
+    ) { innerPadding ->
+        NavHost(
             navController = navController,
-            onAuthSuccess = onAuthSuccess
-        )
-        mainNavGraph(navController = navController)
+            startDestination = startDestination,
+            modifier = modifier.padding(innerPadding)
+        ) {
+            authNavGraph(
+                navController = navController,
+                onAuthSuccess = onAuthSuccess
+            )
+            mainNavGraph(navController = navController)
+        }
     }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt b/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
index db2b43c..1eec75f 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
@@ -1,51 +1,22 @@
 /**
  * 主页面导航图
  *
- * 包含首页等已登录后可见页面的路由配置，以及底部导航栏。
+ * 包含首页等已登录后可见页面的路由配置。
+ * 底部导航栏在 [LianjiNavHost] 层面统一管理，此处不再单独包裹 Scaffold。
  */
 package cn.iven.app.navigation
 
-import android.widget.Toast
-import androidx.compose.foundation.layout.padding
-import androidx.compose.material.icons.Icons
-import androidx.compose.material.icons.automirrored.filled.Chat
-import androidx.compose.material.icons.filled.Book
-import androidx.compose.material.icons.filled.CalendarToday
-import androidx.compose.material.icons.filled.Home
-import androidx.compose.material.icons.filled.Person
-import androidx.compose.material3.Icon
-import androidx.compose.material3.NavigationBar
-import androidx.compose.material3.NavigationBarItem
-import androidx.compose.material3.Scaffold
-import androidx.compose.material3.Text
-import androidx.compose.runtime.Composable
-import androidx.compose.runtime.getValue
-import androidx.compose.ui.Modifier
-import androidx.compose.ui.platform.LocalContext
+import androidx.compose.animation.core.tween
+import androidx.compose.animation.slideInHorizontally
+import androidx.compose.animation.slideOutHorizontally
 import androidx.navigation.NavGraphBuilder
 import androidx.navigation.NavHostController
 import androidx.navigation.compose.composable
-import androidx.navigation.compose.currentBackStackEntryAsState
 import androidx.navigation.navigation
+import cn.iven.app.feature.anniversary.ui.edit.AnniversaryEditScreen
+import cn.iven.app.feature.anniversary.ui.list.AnniversaryListScreen
 import cn.iven.app.feature.home.ui.HomeScreen
 import cn.iven.app.feature.profile.ui.ProfileScreen
-import cn.iven.app.ui.theme.LovePink
-import cn.iven.app.ui.theme.TextSecondaryLight
-
-/** 底部导航项定义 */
-private data class BottomNavItem(
-    val route: String,
-    val label: String,
-    val icon: androidx.compose.ui.graphics.vector.ImageVector
-)
-
-private val bottomNavItems = listOf(
-    BottomNavItem(Routes.HOME, "首页", Icons.Default.Home),
-    BottomNavItem(Routes.NOTE, "记事", Icons.Default.Book),
-    BottomNavItem(Routes.ANNIVERSARY, "纪念日", Icons.Default.CalendarToday),
-    BottomNavItem(Routes.CHAT, "聊天", Icons.AutoMirrored.Filled.Chat),
-    BottomNavItem(Routes.PROFILE, "我的", Icons.Default.Person)
-)
 
 /** 构建主页面模块导航图 */
 fun NavGraphBuilder.mainNavGraph(
@@ -56,70 +27,67 @@ fun NavGraphBuilder.mainNavGraph(
         route = Routes.MAIN
     ) {
         composable(Routes.HOME) {
-            MainScaffold(navController = navController) { modifier ->
-                HomeScreen(modifier = modifier)
-            }
+            HomeScreen(
+                onNavigateToAnniversary = {
+                    navController.navigate(Routes.ANNIVERSARY)
+                }
+            )
         }
-        composable(Routes.PROFILE) {
-            MainScaffold(navController = navController) { modifier ->
-                ProfileScreen(modifier = modifier)
+        composable(Routes.ANNIVERSARY) {
+            AnniversaryListScreen(
+                onNavigateToCreate = {
+                    navController.navigate(Routes.ANNIVERSARY_CREATE)
+                },
+                onNavigateToEdit = { id ->
+                    navController.navigate("${Routes.ANNIVERSARY_EDIT}/$id")
+                }
+            )
+        }
+        composable(
+            Routes.ANNIVERSARY_CREATE,
+            enterTransition = {
+                slideInHorizontally(initialOffsetX = { it }, animationSpec = tween(300))
+            },
+            exitTransition = {
+                slideOutHorizontally(targetOffsetX = { -it }, animationSpec = tween(300))
+            },
+            popEnterTransition = {
+                slideInHorizontally(initialOffsetX = { -it }, animationSpec = tween(300))
+            },
+            popExitTransition = {
+                slideOutHorizontally(targetOffsetX = { it }, animationSpec = tween(300))
             }
+        ) {
+            AnniversaryEditScreen(
+                anniversaryId = null,
+                onSaveSuccess = { navController.popBackStack() },
+                onNavigateBack = { navController.popBackStack() }
+            )
         }
-    }
-}
-
-/**
- * 主页面 Scaffold 布局
- *
- * 包含底部导航栏（首页、记事、纪念日、聊天、我的），包裹主内容区域。
- */
-@Composable
-private fun MainScaffold(
-    navController: NavHostController,
-    content: @Composable (Modifier) -> Unit
-) {
-    val navBackStackEntry by navController.currentBackStackEntryAsState()
-    val currentRoute = navBackStackEntry?.destination?.route
-    val context = LocalContext.current
-
-    Scaffold(
-        bottomBar = {
-            NavigationBar {
-                bottomNavItems.forEach { item ->
-                    val selected = currentRoute == item.route
-                    val isImplemented = item.route == Routes.HOME || item.route == Routes.PROFILE
-
-                    NavigationBarItem(
-                        icon = {
-                            Icon(
-                                imageVector = item.icon,
-                                contentDescription = item.label,
-                                tint = if (selected) LovePink else TextSecondaryLight
-                            )
-                        },
-                        label = {
-                            Text(
-                                text = item.label,
-                                color = if (selected) LovePink else TextSecondaryLight
-                            )
-                        },
-                        selected = selected,
-                        onClick = {
-                            if (isImplemented) {
-                                if (currentRoute != item.route) {
-                                    navController.navigate(item.route) {
-                                        popUpTo(Routes.MAIN) { inclusive = false }
-                                    }
-                                }
-                            } else {
-                                Toast.makeText(context, "功能开发中", Toast.LENGTH_SHORT).show()
-                            }
-                        }
-                    )
-                }
+        composable(
+            "${Routes.ANNIVERSARY_EDIT}/{id}",
+            enterTransition = {
+                slideInHorizontally(initialOffsetX = { it }, animationSpec = tween(300))
+            },
+            exitTransition = {
+                slideOutHorizontally(targetOffsetX = { -it }, animationSpec = tween(300))
+            },
+            popEnterTransition = {
+                slideInHorizontally(initialOffsetX = { -it }, animationSpec = tween(300))
+            },
+            popExitTransition = {
+                slideOutHorizontally(targetOffsetX = { it }, animationSpec = tween(300))
             }
+        ) { backStackEntry ->
+            val id = backStackEntry.arguments?.getString("id")?.toLongOrNull()
+            AnniversaryEditScreen(
+                anniversaryId = id,
+                onSaveSuccess = { navController.popBackStack() },
+                onNavigateBack = { navController.popBackStack() }
+            )
+        }
+        composable(Routes.PROFILE) {
+            ProfileScreen()
         }
-    ) { innerPadding ->
-        content(Modifier.padding(innerPadding))
     }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt b/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
index b554305..351187d 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
@@ -15,6 +15,8 @@ object Routes {
     const val HOME = "main/home"
     const val NOTE = "main/note"
     const val ANNIVERSARY = "main/anniversary"
+    const val ANNIVERSARY_CREATE = "main/anniversary/create"
+    const val ANNIVERSARY_EDIT = "main/anniversary/edit"
     const val CHAT = "main/chat"
     const val PROFILE = "main/profile"
 }
```

### `6b059f19` chore(skill): 更新 api-debug-verify skill 并新增 pgsql-lianji 数据库查询 skill

- **时间:** 2026-05-16 15:53:23 +0800

**提交信息:**

chore(skill): 更新 api-debug-verify skill 并新增 pgsql-lianji 数据库查询 skill

- api-debug-verify: 迁移为 Docker 容器调试验证流程
- pgsql-lianji: 新增项目 PostgreSQL 数据库查询 skill
- docker-compose.yml: 添加 api 服务，支持 DEBUG 模式
- Dockerfile: 支持 JDWP 远程调试端口 8098
- application.yaml: 数据库端口参数化为 DB_PORT

**代码变更:**

```diff
diff --git a/.claude/skills/api-debug-verify/SKILL.md b/.claude/skills/api-debug-verify/SKILL.md
index 5104a01..87a902c 100644
--- a/.claude/skills/api-debug-verify/SKILL.md
+++ b/.claude/skills/api-debug-verify/SKILL.md
@@ -1,210 +1,221 @@
 ---
 name: api-debug-verify
-description: 联机后端 API 服务调试验证流程。用于启动 Spring Boot 后端服务、加载环境变量、验证服务健康状态、通过日志定位问题。Use when: (1) 用户说"启动后端"、"调试API"、"看看后端运行情况"、"后端日志"等，(2) 修改后端代码后需要快速验证服务是否正常启动，(3) 后端出现启动失败、接口异常、数据库连接问题等需要通过日志排查，(4) 需要确认后端服务是否已就绪以配合 App 端调试。
+description: 联机后端 API 服务 Docker 调试验证流程。用于通过 Docker 容器启动 Spring Boot 后端服务、构建镜像、验证服务健康状态、通过容器日志定位问题。Use when: (1) 用户说"启动后端"、"调试API"、"看看后端运行情况"、"后端日志"等，(2) 修改后端代码后需要快速验证服务是否正常启动，(3) 后端出现启动失败、接口异常、数据库连接问题等需要通过日志排查，(4) 需要确认后端服务是否已就绪以配合 App 端调试。
 ---
 
-# 联机后端 API 服务调试验证流程
+# 联机后端 API 服务 Docker 调试验证流程
 
-验证 Spring Boot 后端服务从构建到运行的完整流程。Agent 无法使用断点调试，因此以**日志分析 + 接口验证**为核心手段。
+验证 Spring Boot 后端服务从构建到 Docker 容器运行的完整流程。Agent 无法使用断点调试器附加进程，因此以**日志分析 + 接口验证**为核心手段。
 
 ## 前置检查
 
-### 1. 确认 Java 版本
-
-需要 Java 21：
+### 1. 确认 Docker 环境
 
 ```bash
-java -version
+docker --version
+docker compose version
 ```
 
 ### 2. 确认环境变量文件
 
-环境变量文件位于 `src/api/.env`：
+环境变量文件位于 `docker/.env`：
 
 ```bash
-cat src/api/.env
+cat docker/.env
 ```
 
 应包含以下变量：
-- `DB_HOST` / `DB_USER` / `DB_PASS` — PostgreSQL 连接
-- `REDIS_HOST` / `REDIS_PASS` — Redis 连接
-- `JWT_SECRET` — JWT 签名密钥
+- `POSTGRES_PASSWORD` — PostgreSQL 密码
+- `REDIS_PASSWORD` — Redis 密码（可为空）
+- `JWT_SECRET` — JWT 签名密钥（建议 256 bits 以上）
 
-### 3. 确认依赖服务
+### 3. 确认依赖服务容器
 
-检查 PostgreSQL (端口 5433) 和 Redis (端口 6377) 是否可连接：
+检查 db (PostgreSQL) 和 redis 是否已在 `lianji` compose project 中运行：
 
 ```bash
-nc -z localhost 5433 && echo "PostgreSQL OK" || echo "PostgreSQL 未就绪"
-nc -z localhost 6377 && echo "Redis OK" || echo "Redis 未就绪"
+docker compose -p lianji -f docker/docker-compose.yml ps
 ```
 
----
-
-## Phase 1: 环境准备与构建
+或直接查看容器状态：
 
-### 1. 加载环境变量
+```bash
+docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(db|redis)"
+```
 
-进入 `src/api` 目录，加载 `.env` 文件：
+如果未运行，先启动依赖：
 
 ```bash
-cd src/api
-source .env
+docker compose -p lianji -f docker/docker-compose.yml up -d db redis
 ```
 
-> **Windows 注意**：在 Git Bash / MSYS2 环境中，`source .env` 可直接加载 KEY=VALUE 格式的环境变量。
+---
+
+## Phase 1: 构建 JAR
 
-验证加载成功：
+进入 `src/api` 目录，执行 Gradle 构建：
 
 ```bash
-echo $DB_HOST
-echo $JWT_SECRET
+cd src/api
+./gradlew bootJar --no-daemon -x test
 ```
 
-### 2. 构建项目
+构建产物位置：`src/api/build/libs/api-0.0.1-SNAPSHOT.jar`
+
+验证构建产物：
 
 ```bash
-./gradlew build --no-daemon -x test
+ls -lh build/libs/*.jar
 ```
 
 构建失败时先解决编译错误。
 
 ---
 
-## Phase 2: 启动服务
+## Phase 2: 构建镜像并启动容器
+
+### 标准启动（AI 开发推荐，只看日志）
 
-### 方式 A: 前台运行（调试用，日志实时可见）
+在项目根目录执行：
 
 ```bash
-cd src/api
-source .env
-./gradlew bootRun --no-daemon
+docker compose -p lianji -f docker/docker-compose.yml up -d --build api
 ```
 
-日志直接输出到终端，按 `Ctrl+C` 停止。**推荐用于调试场景**。
+参数说明：
+- `-p lianji`：指定 compose project 名称，确保与 db/redis 共享 `lianji_default` 网络
+- `-f docker/docker-compose.yml`：指定 compose 文件路径
+- `--build`：强制重新构建镜像（代码更新后必须加）
+- `-d`：后台运行
+
+### 人工调试模式（需附加调试器）
 
-### 方式 B: 后台运行（持续服务，配合 App 调试）
+如需开放 8098 端口供 IDE 远程调试：
 
 ```bash
-cd src/api
-source .env
+DEBUG=true docker compose -p lianji -f docker/docker-compose.yml up -d --build api
+```
 
-# 创建日志目录（按时间命名，每次启动独立日志文件）
-mkdir -p ../../logs/api
-LOG_FILE="../../logs/api/$(date +%Y-%m-%d_%H-%M-%S).log"
-echo "日志文件: $LOG_FILE"
+> **注意**：AI Agent 无法使用断点调试器，此模式仅供人工调试使用。
 
-./gradlew bootJar --no-daemon -x test
-java -jar build/libs/api-0.0.1-SNAPSHOT.jar > "$LOG_FILE" 2>&1 &
-echo $! > ../../logs/api/api.pid
+### 仅重启（镜像未变更时）
+
+```bash
+docker compose -p lianji -f docker/docker-compose.yml up -d api
+```
+
+### 停止服务
+
+```bash
+docker compose -p lianji -f docker/docker-compose.yml down api
 ```
 
-停止服务：
+或停止并移除容器：
 
 ```bash
-kill $(cat logs/api/api.pid)
-rm logs/api/api.pid
+docker rm -f api
 ```
 
 ---
 
 ## Phase 3: 健康检查
 
-### 1. 检查服务是否监听端口
+### 1. 检查容器状态
 
 ```bash
-nc -z localhost 8080 && echo "服务已启动" || echo "服务未启动"
+docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep api
 ```
 
-或查看进程：
+预期输出：`api Up ... 0.0.0.0:8098-8099->8098-8099/tcp`
+
+### 2. 检查服务是否监听端口
 
 ```bash
-jps | grep ApiApplication
+nc -z localhost 8099 && echo "服务已启动" || echo "服务未启动"
 ```
 
-### 2. 验证 API 接口
+### 3. 验证 API 接口
 
-测试已知端点（如登录接口）：
+测试已知端点：
 
 ```bash
-curl -s -X POST http://localhost:8080/api/v1/auth/login \
-  -H "Content-Type: application/json" \
-  -d '{"username":"test","password":"test"}'
-```
-
-或简单验证服务存活：
+# 首页统计（需认证，预期 401）
+curl -s http://localhost:8099/api/v1/home/stats
 
-```bash
-curl -s http://localhost:8080 | head -c 200
+# 登录接口（预期参数校验错误 400）
+curl -s -X POST http://localhost:8099/api/v1/auth/login \
+  -H "Content-Type: application/json" \
+  -d '{"email":"test@example.com","password":"test"}'
 ```
 
-> 如果返回 JSON 错误响应（如 404 或 401），说明服务本身已启动，只是路径或认证问题。
+> 返回 401 或 400 的 JSON 错误响应说明服务已启动，只是业务逻辑层面的认证/校验问题。
 
 ---
 
 ## Phase 4: 日志调试
 
-Agent 无法使用 IDE 断点，日志是定位问题的核心手段。
+Agent 无法使用 IDE 断点，容器日志是定位问题的核心手段。
 
 ### 实时查看日志
 
-**前台运行**：日志已在终端输出，直接观察。
-
-**后台运行**：
-
 ```bash
-# 查看最新日志文件
-tail -f logs/api/$(ls -t logs/api/*.log | head -1)
+# 查看最新 50 行
+docker logs api --tail 50
+
+# 持续跟踪（类似 tail -f）
+docker logs api -f
 
-# 或指定具体日志文件
-tail -f logs/api/2026-05-15_14-30-00.log
+# 查看全部日志
+docker logs api
 ```
 
-### 日志级别与过滤策略
+### 日志过滤策略
 
 Spring Boot 日志默认级别为 INFO，`cn.iven.lianji` 和 `org.springframework.security` 已配置为 DEBUG。
 
-| 场景 | 过滤命令 |
-|------|---------|
-| **应用业务日志** | `grep -E "cn.iven.lianji\|DEBUG" $LOG_FILE` |
-| **错误异常** | `grep -E "ERROR\|Exception\|Caused by" $LOG_FILE` |
-| **SQL 执行** | `grep -E "Preparing\|Parameters\|==>" $LOG_FILE` |
-| **Security 过滤链** | `grep "springframework.security" $LOG_FILE` |
-| **启动过程** | `grep -E "Started ApiApplication\|Error\|Failed" $LOG_FILE` |
-| **Flyway 迁移** | `grep -i "flyway" $LOG_FILE` |
-
-> **提示**：若未保留 `$LOG_FILE` 变量，可用 `LOG_FILE=$(ls -t logs/api/*.log | head -1)` 获取最新日志文件。
+| 场景 | 命令 |
+|------|------|
+| **应用业务日志** | `docker logs api 2>&1 | grep -E "cn.iven.lianji\|DEBUG"` |
+| **错误异常** | `docker logs api 2>&1 | grep -E "ERROR\|Exception\|Caused by"` |
+| **SQL 执行** | `docker logs api 2>&1 | grep -E "Preparing\|Parameters\|==>"` |
+| **Security 过滤链** | `docker logs api 2>&1 | grep "springframework.security"` |
+| **启动过程** | `docker logs api 2>&1 | grep -E "Started ApiApplication\|Error\|Failed"` |
+| **Flyway 迁移** | `docker logs api 2>&1 | grep -i "flyway"` |
 
 ### 常见调试场景
 
-**启动失败 / 端口占用**：
+**启动失败 / 端口冲突**：
 
 ```bash
-grep -E "Port 8080|Address already in use|Failed to start" $LOG_FILE
+docker logs api 2>&1 | grep -E "Port 8099|Address already in use|Failed to start"
 ```
 
 **数据库连接失败**：
 
 ```bash
-grep -E "SQLException|Connection refused|FATAL" $LOG_FILE
+docker logs api 2>&1 | grep -E "SQLException|Connection refused|FATAL"
 ```
 
+> 容器内数据库地址应为 `db:5432`（不是 localhost:5433，那是宿主机映射端口）
+
 **Flyway 迁移错误**：
 
 ```bash
-grep -i "flyway" $LOG_FILE | grep -i -E "error|fail|migration"
+docker logs api 2>&1 | grep -i "flyway" | grep -i -E "error|fail|migration"
 ```
 
-**JWT / 认证问题**：
+**JWT 签名错误**（密钥长度不足）：
 
 ```bash
-grep -E "Jwt|Authentication|AccessDenied" $LOG_FILE
+docker logs api 2>&1 | grep -E "WeakKeyException|Jwt|JWT"
 ```
 
+> JWT_SECRET 必须 >= 256 bits（约 32 个字符以上）
+
 **MyBatis SQL 问题**：
 
 ```bash
-grep -E "MyBatis|BadSqlGrammar|SQLSyntaxError" $LOG_FILE
+docker logs api 2>&1 | grep -E "MyBatis|BadSqlGrammar|SQLSyntaxError"
 ```
 
 ### 日志分析要点
@@ -224,10 +235,12 @@ grep -E "MyBatis|BadSqlGrammar|SQLSyntaxError" $LOG_FILE
 ```
 ## 验证结果
 
-- **环境变量加载**: ✅ / ❌
-- **构建**: ✅ / ❌
-- **启动**: ✅ / ❌
-- **端口监听**: ✅ / ❌
+- **Docker 环境**: ✅ / ❌
+- **依赖服务 (db/redis)**: ✅ / ❌
+- **Gradle 构建**: ✅ / ❌
+- **Docker 镜像构建**: ✅ / ❌
+- **容器启动**: ✅ / ❌
+- **端口监听 (8099)**: ✅ / ❌
 - **API 响应**: ✅ / ❌
 - **发现的问题**:
   - [如有，附日志片段]
@@ -240,15 +253,17 @@ grep -E "MyBatis|BadSqlGrammar|SQLSyntaxError" $LOG_FILE
 | 现象 | 排查步骤 |
 |------|---------|
 | 构建失败 | 看 Gradle 错误，检查 Java 21 是否安装、依赖是否可下载 |
-| 端口 8080 被占用 | `lsof -i :8080` 或 `netstat -ano \| findstr 8080` 找到进程并停止 |
-| 数据库连接失败 | 检查 `.env` 中 DB_HOST/DB_USER/DB_PASS；确认 PostgreSQL 端口 5433 可连接 |
-| Redis 连接失败 | 检查 `.env` 中 REDIS_HOST；确认 Redis 端口 6377 可连接 |
+| 镜像构建失败 | 确认 `src/api/build/libs/*.jar` 存在；检查 Dockerfile 语法 |
+| 容器启动后立即退出 | `docker logs api` 看启动错误，常见：JWT_SECRET 太短、数据库连不上 |
+| 端口 8099 被占用 | `lsof -i :8099` 或 `netstat -ano \| findstr 8099` 找到进程并停止 |
+| 数据库连接失败 | 容器内应连 `db:5432`，不是 `localhost:5433`；检查 `docker/.env` 中 POSTGRES_PASSWORD |
+| Redis 连接失败 | 容器内应连 `redis:6379`；检查 REDIS_PASSWORD |
 | Flyway 迁移失败 | 检查 `src/main/resources/db/migration` 脚本语法；对比数据库当前版本 |
-| JWT 签名错误 | 确认 `.env` 中 JWT_SECRET 已设置且长度足够 |
+| JWT 签名错误 (WeakKeyException) | 确认 `docker/.env` 中 JWT_SECRET >= 32 个字符 |
 | 启动后接口 401 | 检查 Security 配置，确认端点是否被放行或需要认证 |
-| 启动后接口 404 | 确认请求路径与 Controller 映射一致，检查 context-path 配置 |
+| 启动后接口 404 | 确认请求路径与 Controller 映射一致 |
 | MyBatis Mapper 绑定失败 | 检查 `@MapperScan` 路径；确认 XML 文件在 `resources/mapper/` 下 |
-| 内存不足启动慢 | 添加 `-Xmx512m` 等 JVM 参数限制内存使用 |
+| 容器名冲突 | 确认 compose 命令带了 `-p lianji`，与其他 project 的容器区分开 |
 
 ---
 
@@ -258,10 +273,12 @@ grep -E "MyBatis|BadSqlGrammar|SQLSyntaxError" $LOG_FILE
 - **构建工具**: Gradle + Spring Boot Gradle Plugin 3.4.0
 - **Java 版本**: 21
 - **启动类**: `cn.iven.lianji.ApiApplication`
-- **服务端口**: 8080
-- **环境变量文件**: `src/api/.env`
-- **日志目录**: `logs/api/YYYY-MM-DD_HH-MM-SS.log`（每次启动独立文件，按时间排序）
-- **PID 文件**: `logs/api/api.pid`
-- **依赖服务**: PostgreSQL (端口 5433)、Redis (端口 6377)
+- **服务端口**: 8099
+- **调试端口**: 8098（仅 DEBUG=true 时开放）
+- **Dockerfile**: `src/api/Dockerfile`
+- **Compose 文件**: `docker/docker-compose.yml`
+- **环境变量文件**: `docker/.env`
+- **Compose Project**: `lianji`（必须统一，否则容器名/网络冲突）
+- **依赖服务**: PostgreSQL (宿主机端口 5433，容器内 db:5432)、Redis (宿主机端口 6377，容器内 redis:6379)
 - **技术栈**: Spring Boot 3.4 + Spring Security + JWT + MyBatis Plus + Flyway + Redis
 - **日志配置**: `cn.iven.lianji` DEBUG，`org.springframework.security` DEBUG，MyBatis SQL 输出到控制台
diff --git a/.claude/skills/pgsql-lianji/references/schema.md b/.claude/skills/pgsql-lianji/references/schema.md
new file mode 100644
index 0000000..c39e7a9
--- /dev/null
+++ b/.claude/skills/pgsql-lianji/references/schema.md
@@ -0,0 +1,56 @@
+# 联机项目数据库结构参考
+
+数据库：`lianji` | 地址：`localhost:5433` | 用户：`postgres`
+
+## 表清单
+
+| 表名 | 说明 | 记录数估算 |
+|------|------|-----------|
+| `app_user` | 用户表 | 按实际查询 |
+| `couple_relationship` | 情侣关系表 | 按实际查询 |
+| `flyway_schema_history` | Flyway 迁移历史 | 固定 |
+
+## 表结构
+
+### app_user
+
+| 字段 | 类型 | 约束 |
+|------|------|------|
+| `id` | bigint | PK, auto increment |
+| `email` | varchar(255) | unique, not null |
+| `password_hash` | varchar(255) | not null |
+| `nickname` | varchar(100) | |
+| `avatar_url` | varchar(500) | |
+
+索引：`idx_app_user_email` (btree on email)
+
+### couple_relationship
+
+| 字段 | 类型 | 约束 |
+|------|------|------|
+| `id` | bigint | PK, auto increment |
+| `user_a_id` | bigint | FK → app_user(id), not null |
+| `user_b_id` | bigint | FK → app_user(id), not null |
+| `created_at` | timestamptz | default now(), not null |
+
+约束：`chk_couple_different_users` (user_a_id <> user_b_id)
+索引：`idx_couple_user_a` (unique), `idx_couple_user_b` (unique)
+
+### flyway_schema_history
+
+标准 Flyway 表，记录已执行的迁移版本。
+
+## 关系图
+
+```
+app_user (1) ----< couple_relationship >---- (1) app_user
+       id              user_a_id                  id
+                       user_b_id
+```
+
+## 当前迁移版本
+
+| version | description | installed_on | success |
+|---------|-------------|--------------|---------|
+| 1 | init user and couple | 2026-05-15 03:18:50 | true |
+| 1.1 | remove audit fields | 2026-05-15 23:03:18 | true |
diff --git a/.claude/skills/pgsql-lianji/skill.md b/.claude/skills/pgsql-lianji/skill.md
new file mode 100644
index 0000000..bf04511
--- /dev/null
+++ b/.claude/skills/pgsql-lianji/skill.md
@@ -0,0 +1,99 @@
+---
+name: pgsql-lianji
+description: 联机项目 PostgreSQL 数据库查询工具。用于连接项目本地开发数据库（localhost:5433/lianji）查看表结构、查询数据、验证迁移状态、排查数据问题。Use when: (1) 用户需要查询数据库表数据或表结构，(2) 需要验证 Flyway 迁移是否成功，(3) 排查数据相关问题如用户/情侣关系数据，(4) 确认数据库当前状态，(5) 检查表结构与代码映射是否一致。
+---
+
+# 联机项目 PostgreSQL 数据库查询
+
+## 安全须知
+
+- **绝不将密码硬编码到本 skill 或任何项目文件中**
+- 密码从 `docker/.env` 文件动态读取
+- 查询结果中若包含敏感字段（password_hash 等），避免在对话中完整展示
+- 使用 `PGPASSWORD` 环境变量传递密码，避免密码出现在 shell 历史记录中
+
+## 前置检查
+
+确认 PostgreSQL 容器正在运行：
+
+```bash
+docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep db
+```
+
+预期看到 `db Up ... 0.0.0.0:5433->5432/tcp`。若未运行，先启动：
+
+```bash
+docker compose -p lianji -f docker/docker-compose.yml up -d db
+```
+
+## 获取数据库密码
+
+从环境变量文件读取（**只读取，不输出到对话**）：
+
+```bash
+# 读取密码到变量，不要在对话中 echo
+POSTGRES_PASSWORD=$(grep "^POSTGRES_PASSWORD=" docker/.env | cut -d= -f2)
+```
+
+> 读取后直接使用变量，不要打印密码值。
+
+## 连接与常用查询
+
+所有命令使用 `psql` 连接 `localhost:5433`，数据库为 `lianji`，用户为 `postgres`。
+
+### 1. 查看所有表
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji -c "\dt"
+```
+
+### 2. 查看某表结构
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji -c "\d <表名>"
+```
+
+### 3. 查询表数据
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji -c "SELECT * FROM <表名> LIMIT 10;"
+```
+
+### 4. 查看 Flyway 迁移历史
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji -c "SELECT version, description, installed_on, success FROM flyway_schema_history ORDER BY installed_rank;"
+```
+
+### 5. 统计各表记录数
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji -c "
+SELECT schemaname, relname, n_live_tup
+FROM pg_stat_user_tables
+WHERE schemaname = 'public'
+ORDER BY n_live_tup DESC;
+"
+```
+
+### 6. 进入交互式 psql 会话
+
+```bash
+PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -p 5433 -U postgres -d lianji
+```
+
+## 表结构参考
+
+详细表结构、字段说明、索引和外键约束参见 [references/schema.md](references/schema.md)。
+
+在不确定表结构时先读取该文件，避免重复查询。
+
+## 项目上下文
+
+- **数据库名**: `lianji`
+- **宿主机端口**: `5433`（容器内为 `5432`）
+- **用户名**: `postgres`
+- **密码来源**: `docker/.env` 中 `POSTGRES_PASSWORD`
+- **依赖**: `db` 容器必须在 `lianji` compose project 中运行
+- **Flyway 迁移脚本位置**: `src/api/src/main/resources/db/migration/`
+- **当前表**: `app_user`、`couple_relationship`、`flyway_schema_history`
diff --git a/docker/docker-compose.yml b/docker/docker-compose.yml
index d00e901..c541d92 100644
--- a/docker/docker-compose.yml
+++ b/docker/docker-compose.yml
@@ -46,6 +46,29 @@ services:
       timeout: 5s
       retries: 5
 
+  api:
+    build:
+      context: ../src/api
+      dockerfile: Dockerfile
+    container_name: api
+    restart: unless-stopped
+    environment:
+      DB_HOST: db
+      DB_USER: postgres
+      DB_PASS: ${POSTGRES_PASSWORD}
+      REDIS_HOST: redis
+      REDIS_PASS: ${REDIS_PASSWORD:-}
+      JWT_SECRET: ${JWT_SECRET:-change-me-in-production-please-use-a-long-and-random-string-for-jwt-signing}
+      DEBUG: ${DEBUG:-false}
+    ports:
+      - "8099:8099"
+      - "8098:8098"
+    depends_on:
+      db:
+        condition: service_healthy
+      redis:
+        condition: service_healthy
+
 volumes:
   postgres_data:
   redis_data:
diff --git a/src/api/Dockerfile b/src/api/Dockerfile
new file mode 100644
index 0000000..c709f38
--- /dev/null
+++ b/src/api/Dockerfile
@@ -0,0 +1,12 @@
+FROM eclipse-temurin:21-jre-alpine
+
+WORKDIR /app
+
+COPY build/libs/*.jar app.jar
+
+EXPOSE 8099
+EXPOSE 8098
+
+ENV DEBUG=false
+
+ENTRYPOINT ["sh", "-c", "if [ \"$DEBUG\" = \"true\" ]; then java -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8098 -jar app.jar; else java -jar app.jar; fi"]
diff --git a/src/api/src/main/resources/application.yaml b/src/api/src/main/resources/application.yaml
index 2adb567..a126955 100644
--- a/src/api/src/main/resources/application.yaml
+++ b/src/api/src/main/resources/application.yaml
@@ -2,7 +2,7 @@ spring:
   application:
     name: api
   datasource:
-    url: jdbc:postgresql://${DB_HOST:localhost}:5433/lianji
+    url: jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/lianji
     username: ${DB_USER:postgres}
     password: ${DB_PASS:postgres}
     driver-class-name: org.postgresql.Driver
```

### `9306f47c` chore(config): 后端与前端端口统一调整为 8099

- **时间:** 2026-05-16 14:59:37 +0800

**提交信息:**

chore(config): 后端与前端端口统一调整为 8099

- application.yaml: server.port 8080 → 8099
- NetworkModule.kt: BASE_URL 8080 → 8099

**代码变更:**

```diff
diff --git a/src/api/src/main/resources/application.yaml b/src/api/src/main/resources/application.yaml
index 4fa0c7d..2adb567 100644
--- a/src/api/src/main/resources/application.yaml
+++ b/src/api/src/main/resources/application.yaml
@@ -35,7 +35,7 @@ mybatis-plus:
       logic-not-delete-value: 0
 
 server:
-  port: 8080
+  port: 8099
 
 app:
   jwt:
diff --git a/src/app/app/src/main/java/cn/iven/app/di/NetworkModule.kt b/src/app/app/src/main/java/cn/iven/app/di/NetworkModule.kt
index 54278c9..b621cab 100644
--- a/src/app/app/src/main/java/cn/iven/app/di/NetworkModule.kt
+++ b/src/app/app/src/main/java/cn/iven/app/di/NetworkModule.kt
@@ -31,7 +31,7 @@ import javax.inject.Singleton
 @InstallIn(SingletonComponent::class)
 object NetworkModule {
 
-    private const val BASE_URL = "http://10.0.2.2:8080/"
+    private const val BASE_URL = "http://10.0.2.2:8099/"
 
     @Provides
     @Singleton
```

### `e343c4cf` chore(openspec): 归档 home-page-with-mock-backend 变更

- **时间:** 2026-05-16 00:49:24 +0800

**提交信息:**

chore(openspec): 归档 home-page-with-mock-backend 变更

- 归档完整变更至 openspec/changes/archive/2026-05-15-home-page-with-mock-backend/
- 同步 delta specs 至 openspec/specs/（home-screen-ui、home-stats-api）

**代码变更:**

```diff
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/.openspec.yaml b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/.openspec.yaml
new file mode 100644
index 0000000..9f70866
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/.openspec.yaml
@@ -0,0 +1,2 @@
+schema: spec-driven
+created: 2026-05-15
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/design.md b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/design.md
new file mode 100644
index 0000000..725824f
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/design.md
@@ -0,0 +1,59 @@
+## Context
+
+Phase 1（认证体系）已归档，后端建立了完整的 DDD 四层架构（API → Application → Domain → Infrastructure），Android 端建立了 MVVM + Repository + Hilt 的模块化架构。当前数据库仅有 `app_user` 和 `couple_relationship` 两张表，记事、纪念日、成就、聊天模块均未开始。
+
+首页是用户绑定情侣后的默认落地页，聚合展示多维度恋爱数据。由于依赖模块的表尚未创建，本次采用**后端 Service 层 Mock 数据**的策略，先建立完整的 API 契约和前端 UI，后续替换为真实聚合查询时前端零改动。
+
+## Goals / Non-Goals
+
+**Goals：**
+- 建立 `GET /api/v1/home/stats` 的完整后端链路（Controller → DTO → AppService → Result）
+- 确定首页 API 响应结构，兼容后续真实数据源
+- 实现 Android 首页完整 UI（统计卡片 + 纪念日提醒 + 时间线）
+- 首页数据通过后端 Mock 返回，前端按真实 API 开发
+
+**Non-Goals：**
+- 不创建新的数据库表（memory、anniversary 等留给后续 Phase）
+- 不实现真实的聚合查询逻辑（COUNT / DISTINCT 等 SQL 聚合）
+- 不实现图片上传/头像功能
+- 不涉及 WebSocket 聊天消息的实时推送
+- 不修改现有认证模块的任何代码
+
+## Decisions
+
+### 1. 后端 Mock 数据放在 AppService 层
+**选择**：在 `HomeAppServiceImpl.getStats()` 中直接返回构造好的 `HomeStatsResult`，不走数据库查询。
+**理由**：
+- Controller、DTO、Result 对象的定义与真实实现完全一致，后续只需替换 Service 实现
+- 前端不需要任何 Mock 代码，HomeRepository 直接调用真实 API
+- 符合现有 DDD 分层，不破坏架构约定
+
+### 2. 响应结构采用扁平 DTO，内联列表数据
+**选择**：单个接口返回所有首页所需数据（统计卡片 + 时间线 + 纪念日），而不是拆分为 3 个接口。
+**理由**：
+- 首页是只读聚合页，数据量小，一次请求减少网络往返
+- 5 个统计项 + 最近 5 条记事 + 最近 1 个纪念日，数据量控制在 KB 级别
+- 后续如需分页，可在 `recentMemories` 上扩展分页参数
+
+**替代方案**：拆分为 `/stats/cards`、`/stats/timeline`、`/stats/upcoming` 三个接口。
+**不选原因**：首页加载需要 3 次串行/并行请求，增加复杂度和加载时间。
+
+### 3. Android 端使用独立的 HomeUiState 管理三个区块
+**选择**：`HomeUiState` 包含 `statsCards`、`upcomingAnniversary`、`recentMemories` 三个字段，各自有独立的加载/成功/错误状态。
+**理由**：
+- 首页三个区块独立渲染，一个区块失败不应影响其他区块展示
+- 统计卡片可以优先显示（来自 couple_relationship 的真实数据），时间线和纪念日可以后加载
+- 符合 Compose 的细粒度重组优化
+
+### 4. 时间线卡片的颜色圆点代表心情值
+**选择**：`mood` 字段 1-5 映射为 5 种颜色（粉/紫/橙/绿/蓝），在 UI 上表现为时间线左侧的彩色圆点。
+**理由**：设计稿中时间线卡片已有彩色圆点（🔴🟣），与心情值天然对应，无需额外图标字段。
+
+## Risks / Trade-offs
+
+| 风险 | 缓解措施 |
+|------|---------|
+| Mock 数据结构与实际表结构不一致，后续需改动 DTO | 严格对照需求文档中的数据模型设计 DTO，预留扩展字段；替换前进行兼容性检查 |
+| 首页接口一次性返回过多数据，后续数据量大时性能差 | 当前数据量极小无需担心；后续在 `recentMemories` 上增加分页参数 `limit`，保持向后兼容 |
+| Android 首页 UI 复杂（三个区块），首次 Compose 实现可能性能不佳 | 使用 `LazyColumn` 懒加载；统计卡片用 `Row` 而非 `LazyRow`（固定 5 个）；后续可用 remember/derivedStateOf 优化 |
+| 底部导航 5 个 Tab 只有首页有内容，其余点击无反应 | 暂时 Toast 提示"功能开发中"，不阻塞首页交付 |
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/proposal.md b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/proposal.md
new file mode 100644
index 0000000..5e367a5
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/proposal.md
@@ -0,0 +1,30 @@
+## Why
+
+Phase 1（认证体系）已完成后，用户绑定情侣后的第一站就是首页。首页是产品的核心体验入口，聚合展示恋爱数据（在一起天数、记录数、纪念日提醒、最近记事时间线）。没有首页，用户完成绑定后面对空白页面，产品价值无法传达。需要尽快建立首页的完整数据链路 + UI 呈现。
+
+## What Changes
+
+- **新增后端 API**：`GET /api/v1/home/stats` 首页统计接口，使用 Mock 数据返回（后续替换为真实聚合查询）
+  - 统计卡片数据：在一起天数、记录数、地点数、消息数、成就数
+  - 即将到来的纪念日列表
+  - 最近记事时间线（分页）
+- **新增后端 DTO / AppService / Controller**：建立首页完整的 DDD 四层链路骨架
+- **新增 Android 首页 UI**：统计卡片、纪念日提醒卡片、时间线列表
+- **新增 Android 数据层**：HomeApi、HomeRepository、HomeViewModel、HomeUiState
+- **底部导航栏更新**：首页 Tab 成为默认落地页，展示真实数据
+
+## Capabilities
+
+### New Capabilities
+- `home-stats-api`: 后端首页统计聚合 API，定义响应结构（统计卡片 + 时间线 + 纪念日），当前使用 Mock 数据填充
+- `home-screen-ui`: Android 首页完整 UI 实现，包含统计卡片、即将到来纪念日、最近记录时间线三个区块
+
+### Modified Capabilities
+- （无现有 capability 需要修改）
+
+## Impact
+
+- **后端**：新增 `HomeController`、`HomeAppService`、`HomeStatsResponseDTO` 等，不影响现有认证模块
+- **Android**：`HomeScreen.kt` 从占位文本替换为完整实现，新增 `feature/home` 模块下的 ViewModel/Repository/Api
+- **数据库**：本次不新增表（Mock 数据），但 DTO 结构设计需兼容后续 `memory`、`anniversary`、`achievement`、`chat_message` 表的真实查询
+- **API 契约**：`GET /api/v1/home/stats` 响应结构一旦确定，后续真实实现需保持兼容
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-screen-ui/spec.md b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-screen-ui/spec.md
new file mode 100644
index 0000000..ee326b3
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-screen-ui/spec.md
@@ -0,0 +1,59 @@
+## ADDED Requirements
+
+### Requirement: Home screen displays statistics cards
+The home screen SHALL display 5 statistics cards arranged in a grid layout with 3 cards on the first row and 2 cards on the second row.
+
+#### Scenario: Stats cards rendered
+- **WHEN** the user navigates to the home screen
+- **THEN** the system displays cards for days together, memory count, location count, message count, and achievement count with distinct colors
+
+#### Scenario: Stats cards loading state
+- **WHEN** the home stats data is being fetched
+- **THEN** the system shows shimmer/placeholder loading indicators on the stats cards
+
+### Requirement: Home screen displays upcoming anniversary section
+The home screen SHALL display a section titled "即将到来" with the nearest upcoming anniversary.
+
+#### Scenario: Upcoming anniversary visible
+- **WHEN** there is an upcoming anniversary within 30 days
+- **THEN** the system displays an anniversary card with icon, title, and remaining days in pink accent color
+
+#### Scenario: No upcoming anniversary
+- **WHEN** there are no upcoming anniversaries
+- **THEN** the system displays an empty state message or hides the section
+
+### Requirement: Home screen displays recent memories timeline
+The home screen SHALL display a "最近记录" section with recent memory entries in timeline format.
+
+#### Scenario: Timeline entries rendered
+- **WHEN** there are recent memory records
+- **THEN** the system displays each entry with a colored mood dot, title, description snippet, and date
+
+#### Scenario: Timeline empty state
+- **WHEN** there are no memory records
+- **THEN** the system displays an empty state prompting the user to create their first memory
+
+### Requirement: Color-coded mood indicators
+Each timeline entry SHALL display a colored dot corresponding to the memory's mood value.
+
+#### Scenario: Mood color mapping
+- **WHEN** a memory entry has mood value 1-5
+- **THEN** the system displays the corresponding color: 1=pink, 2=purple, 3=orange, 4=green, 5=blue
+
+### Requirement: Pull-to-refresh functionality
+The home screen SHALL support pull-to-refresh to reload all data.
+
+#### Scenario: User pulls to refresh
+- **WHEN** the user performs a pull-to-refresh gesture
+- **THEN** the system re-fetches home stats data and updates all sections
+
+### Requirement: Error handling per section
+Each section SHALL handle errors independently without crashing the entire screen.
+
+#### Scenario: Network error on stats cards
+- **WHEN** the stats cards data fails to load
+- **THEN** the system displays an error state on stats cards while other sections remain visible
+
+#### Scenario: Network error on timeline
+- **WHEN** the timeline data fails to load
+- **THEN** the system displays a retry button on the timeline section while stats cards remain visible
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-stats-api/spec.md b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-stats-api/spec.md
new file mode 100644
index 0000000..aac5902
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/specs/home-stats-api/spec.md
@@ -0,0 +1,60 @@
+## ADDED Requirements
+
+### Requirement: Home stats API returns aggregated data
+The system SHALL expose `GET /api/v1/home/stats` that returns aggregated home page data for the authenticated user.
+
+#### Scenario: Authenticated user requests home stats
+- **WHEN** an authenticated user sends GET /api/v1/home/stats
+- **THEN** the system returns HTTP 200 with a response containing stats cards, upcoming anniversaries, and recent memories
+
+### Requirement: Stats cards include five metrics
+The response SHALL include exactly five statistics: days together, memory count, location count, message count, and achievement count.
+
+#### Scenario: Days together calculation
+- **WHEN** the user has an active couple relationship
+- **THEN** the system calculates days together from couple_relationship.created_at to current date
+
+#### Scenario: Memory count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of memory records for the couple
+
+#### Scenario: Location count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the count of distinct locations across all memory records for the couple
+
+#### Scenario: Message count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of chat messages exchanged between the couple
+
+#### Scenario: Achievement count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of unlocked achievements for the couple
+
+### Requirement: Upcoming anniversary section
+The response SHALL include a list of upcoming anniversaries sorted by nearest date.
+
+#### Scenario: Anniversary within 30 days
+- **WHEN** there is an anniversary occurring within 30 days
+- **THEN** the response includes the anniversary title and remaining days
+
+#### Scenario: No upcoming anniversary
+- **WHEN** there are no anniversaries within the upcoming window
+- **THEN** the response includes an empty list for upcoming anniversaries
+
+### Requirement: Recent memories timeline
+The response SHALL include recent memory records in reverse chronological order.
+
+#### Scenario: Recent memories with pagination
+- **WHEN** the user requests home stats
+- **THEN** the response includes the most recent 5 memory records with title, description snippet, date, and mood
+
+#### Scenario: Empty memory timeline
+- **WHEN** the couple has no memory records
+- **THEN** the response includes an empty list for recent memories
+
+### Requirement: Service layer uses mock data
+The AppService implementation SHALL return statically constructed data that matches the response schema.
+
+#### Scenario: Mock data consistency
+- **WHEN** the home stats endpoint is called
+- **THEN** the response structure and data types SHALL match the production schema exactly, with only the data values being mock
diff --git a/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/tasks.md b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/tasks.md
new file mode 100644
index 0000000..183b1cf
--- /dev/null
+++ b/openspec/changes/archive/2026-05-15-home-page-with-mock-backend/tasks.md
@@ -0,0 +1,177 @@
+## 1. 后端 — 首页统计 API 骨架
+
+### 1.1 定义响应 DTO 与 Result 对象
+
+**测试边界**
+- 输入条件：已登录用户（JWT 认证通过）
+- 前置状态：用户已绑定情侣关系
+- 后置状态：返回结构正确的首页统计数据
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-001 | 正常请求 | 已认证用户 | 返回 HomeStatsResponseDTO，包含5个统计项、时间线、纪念日 | - |
+| TC-002 | 未认证请求 | 无 Token | - | 401 Unauthorized |
+
+**实现步骤**
+- [x] 1.1.1 创建 `HomeStatsResult.java`（应用层结果对象：daysTogether, memoryCount, locationCount, messageCount, achievementCount, upcomingAnniversaries, recentMemories）
+- [x] 1.1.2 创建 `HomeStatsResponseDTO.java`（API 层响应 DTO）
+- [x] 1.1.3 创建 `AnniversaryCardDTO.java`（纪念日卡片：title, remainingDays）
+- [x] 1.1.4 创建 `MemoryTimelineItemDTO.java`（时间线项：id, title, description, date, mood）
+
+### 1.2 实现应用层 Service（Mock 数据）
+
+**测试边界**
+- 输入条件：任意已认证用户 ID
+- 前置状态：Service 已注入 CoupleRepository
+- 后置状态：返回固定 Mock 数据，数据结构符合 DTO 定义
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-003 | Mock 数据返回 | userId=1 | daysTogether 从 couple_relationship.created_at 计算，其余为固定 Mock 值 | - |
+| TC-004 | 未绑定情侣 | userId=未绑定 | - | 抛出 BusinessException(403) |
+
+**实现步骤**
+- [x] 1.2.1 创建 `HomeAppService.java` 接口（`HomeStatsResult getStats(Long userId)`）
+- [x] 1.2.2 创建 `HomeAppServiceImpl.java`，实现 Mock 数据返回
+  - daysTogether：从 couple_relationship.created_at 到当前日期计算（真实逻辑）
+  - memoryCount/locationCount/messageCount/achievementCount：固定 Mock 值
+  - upcomingAnniversaries：返回 1 条 Mock 数据
+  - recentMemories：返回 3 条 Mock 数据，mood 值 1-3
+- [x] 1.2.3 注入 `CoupleRepository` 查询当前用户的情侣关系
+
+### 1.3 实现 API 层 Controller
+
+**测试边界**
+- 输入条件：HTTP GET /api/v1/home/stats，带 Bearer Token
+- 前置状态：用户已登录且已绑定情侣
+- 后置状态：返回 HTTP 200 + ResponseMessage<HomeStatsResponseDTO>
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-005 | 正常请求 | 有效 Access Token | code=200, data 包含完整统计 | - |
+| TC-006 | Token 过期 | 过期 Token | - | 401，触发刷新逻辑 |
+
+**实现步骤**
+- [x] 1.3.1 创建 `HomeController.java`，`@GetMapping("/api/v1/home/stats")`
+- [x] 1.3.2 注入 `HomeAppService`，调用 getStats 并转换 DTO
+- [x] 1.3.3 添加 `@RequiresPermission` 或 Spring Security 配置（需认证）
+- [x] 1.3.4 创建 DTO ↔ Result 转换器 `HomeResponseConverter.java`
+
+---
+
+## 2. Android — 首页数据层
+
+### 2.1 网络层定义
+
+**测试边界**
+- 输入条件：已登录用户（DataStore 中有有效 Token）
+- 前置状态：Retrofit 已配置 BaseURL 和 AuthInterceptor
+- 后置状态：成功解析后端返回的 JSON
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-007 | 正常请求 | 启动首页 | 返回 HomeStatsDto | - |
+| TC-008 | 网络异常 | 无网络连接 | - | 返回 NetworkError |
+
+**实现步骤**
+- [x] 2.1.1 创建 `HomeStatsDto.kt`（数据类：statsCards, upcomingAnniversary, recentMemories）
+- [x] 2.1.2 创建 `HomeApi.kt`（Retrofit 接口：`@GET("home/stats")`）
+- [x] 2.1.3 创建 `StatsCardDto.kt`、`AnniversaryCardDto.kt`、`MemoryTimelineItemDto.kt`
+
+### 2.2 Repository 与 DI 模块
+
+**测试边界**
+- 输入条件：调用 `getHomeStats()`
+- 前置状态：HomeApi 可用
+- 后置状态：返回 Domain 层的 `HomeStats` 对象
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-009 | 正常获取 | - | 返回 HomeStats 领域对象 | - |
+| TC-010 | API 返回错误 | 后端 500 | - | 返回 RepositoryError |
+
+**实现步骤**
+- [x] 2.2.1 创建 `HomeRepository.kt` 接口（`suspend fun getHomeStats(): Result<HomeStats>`）
+- [x] 2.2.2 创建 `HomeRepositoryImpl.kt`，调用 HomeApi 并做 DTO → Domain 转换
+- [x] 2.2.3 创建 `HomeModule.kt`（Hilt 模块，绑定 Repository）
+- [x] 2.2.4 创建 Domain 层 `HomeStats.kt`、`StatsCard.kt`、`AnniversaryCard.kt`、`MemoryTimelineItem.kt`
+
+---
+
+## 3. Android — 首页 UI 层
+
+### 3.1 ViewModel 与状态管理
+
+**测试边界**
+- 输入条件：用户进入首页
+- 前置状态：ViewModel 已注入 HomeRepository
+- 后置状态：UI State 从 Loading → Success 过渡
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-011 | 正常加载 | 进入首页 | UiState 变为 Success，数据展示正确 | - |
+| TC-012 | 下拉刷新 | 下拉手势 | 重新触发加载，数据刷新 | - |
+| TC-013 | 网络错误 | 无网络 | 显示 Snackbar 错误提示，保留上次数据 | - |
+
+**实现步骤**
+- [x] 3.1.1 创建 `HomeUiState.kt`（sealed class：Loading, Success, Error）
+- [x] 3.1.2 创建 `HomeUiEvent.kt`（Refresh, Retry）
+- [x] 3.1.3 创建 `HomeViewModel.kt`，暴露 `uiState: StateFlow<HomeUiState>`
+- [x] 3.1.4 实现 `loadStats()` 和 `refresh()` 方法
+
+### 3.2 首页 Screen 与组件
+
+**测试边界**
+- 输入条件：HomeUiState 为 Success
+- 前置状态：数据已加载
+- 后置状态：屏幕完整渲染设计稿中的所有元素
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-014 | 完整渲染 | Success 状态 | 显示统计卡片、纪念日卡片、时间线 | - |
+| TC-015 | 空时间线 | memories 为空 | 显示空状态提示 | - |
+| TC-016 | Mood 颜色映射 | mood=1~5 | 圆点颜色分别为粉/紫/橙/绿/蓝 | - |
+
+**实现步骤**
+- [x] 3.2.1 重写 `HomeScreen.kt`，接入 ViewModel 和 uiState
+- [x] 3.2.2 创建 `StatsCardsSection.kt`（统计卡片网格：3+2 布局，5 种颜色）
+- [x] 3.2.3 创建 `UpcomingAnniversarySection.kt`（即将到来区域）
+- [x] 3.2.4 创建 `RecentMemoriesSection.kt`（时间线列表，带彩色 mood 圆点）
+- [x] 3.2.5 实现 Pull-to-Refresh（`PullRefreshIndicator` 或 `SwipeRefresh`）
+- [x] 3.2.6 实现 Error Snackbar 和空状态
+
+### 3.3 导航与集成
+
+**测试边界**
+- 输入条件：用户完成绑定后进入首页
+- 前置状态：已登录且已绑定
+- 后置状态：首页作为默认 Tab 正确展示
+
+**测试用例**
+| 用例ID | 场景 | 输入 | 期望输出/行为 | 异常 |
+|--------|------|------|---------------|------|
+| TC-017 | 默认 Tab | 绑定完成后 | 底部导航高亮"首页"，展示统计卡片 | - |
+| TC-018 | Tab 切换 | 点击其他 Tab | 暂时 Toast"功能开发中" | - |
+
+**实现步骤**
+- [x] 3.3.1 更新 `MainNavGraph.kt`，确保首页路由正确
+- [x] 3.3.2 未实现 Tab（记事/纪念日/聊天）点击时显示 Toast 提示
+- [x] 3.3.3 验证从绑定页跳转后首页数据正确加载
+
+---
+
+## 4. 联调与验收
+
+- [x] 4.1 启动后端服务，验证 `GET /api/v1/home/stats` 返回正确 JSON 结构
+- [x] 4.2 启动 Android App，验证首页 UI 渲染与设计稿一致
+- [x] 4.3 验证 Token 失效时自动刷新并重试
+- [x] 4.4 验证网络异常时的错误状态展示
+- [x] 4.5 运行后端单元测试（HomeAppServiceImpl）
+- [x] 4.6 截图对比设计稿，确认视觉还原度
diff --git a/openspec/specs/home-screen-ui/spec.md b/openspec/specs/home-screen-ui/spec.md
new file mode 100644
index 0000000..1737484
--- /dev/null
+++ b/openspec/specs/home-screen-ui/spec.md
@@ -0,0 +1,63 @@
+# home-screen-ui Specification
+
+## Purpose
+TBD - created by archiving change home-page-with-mock-backend. Update Purpose after archive.
+## Requirements
+### Requirement: Home screen displays statistics cards
+The home screen SHALL display 5 statistics cards arranged in a grid layout with 3 cards on the first row and 2 cards on the second row.
+
+#### Scenario: Stats cards rendered
+- **WHEN** the user navigates to the home screen
+- **THEN** the system displays cards for days together, memory count, location count, message count, and achievement count with distinct colors
+
+#### Scenario: Stats cards loading state
+- **WHEN** the home stats data is being fetched
+- **THEN** the system shows shimmer/placeholder loading indicators on the stats cards
+
+### Requirement: Home screen displays upcoming anniversary section
+The home screen SHALL display a section titled "即将到来" with the nearest upcoming anniversary.
+
+#### Scenario: Upcoming anniversary visible
+- **WHEN** there is an upcoming anniversary within 30 days
+- **THEN** the system displays an anniversary card with icon, title, and remaining days in pink accent color
+
+#### Scenario: No upcoming anniversary
+- **WHEN** there are no upcoming anniversaries
+- **THEN** the system displays an empty state message or hides the section
+
+### Requirement: Home screen displays recent memories timeline
+The home screen SHALL display a "最近记录" section with recent memory entries in timeline format.
+
+#### Scenario: Timeline entries rendered
+- **WHEN** there are recent memory records
+- **THEN** the system displays each entry with a colored mood dot, title, description snippet, and date
+
+#### Scenario: Timeline empty state
+- **WHEN** there are no memory records
+- **THEN** the system displays an empty state prompting the user to create their first memory
+
+### Requirement: Color-coded mood indicators
+Each timeline entry SHALL display a colored dot corresponding to the memory's mood value.
+
+#### Scenario: Mood color mapping
+- **WHEN** a memory entry has mood value 1-5
+- **THEN** the system displays the corresponding color: 1=pink, 2=purple, 3=orange, 4=green, 5=blue
+
+### Requirement: Pull-to-refresh functionality
+The home screen SHALL support pull-to-refresh to reload all data.
+
+#### Scenario: User pulls to refresh
+- **WHEN** the user performs a pull-to-refresh gesture
+- **THEN** the system re-fetches home stats data and updates all sections
+
+### Requirement: Error handling per section
+Each section SHALL handle errors independently without crashing the entire screen.
+
+#### Scenario: Network error on stats cards
+- **WHEN** the stats cards data fails to load
+- **THEN** the system displays an error state on stats cards while other sections remain visible
+
+#### Scenario: Network error on timeline
+- **WHEN** the timeline data fails to load
+- **THEN** the system displays a retry button on the timeline section while stats cards remain visible
+
diff --git a/openspec/specs/home-stats-api/spec.md b/openspec/specs/home-stats-api/spec.md
new file mode 100644
index 0000000..c64798b
--- /dev/null
+++ b/openspec/specs/home-stats-api/spec.md
@@ -0,0 +1,64 @@
+# home-stats-api Specification
+
+## Purpose
+TBD - created by archiving change home-page-with-mock-backend. Update Purpose after archive.
+## Requirements
+### Requirement: Home stats API returns aggregated data
+The system SHALL expose `GET /api/v1/home/stats` that returns aggregated home page data for the authenticated user.
+
+#### Scenario: Authenticated user requests home stats
+- **WHEN** an authenticated user sends GET /api/v1/home/stats
+- **THEN** the system returns HTTP 200 with a response containing stats cards, upcoming anniversaries, and recent memories
+
+### Requirement: Stats cards include five metrics
+The response SHALL include exactly five statistics: days together, memory count, location count, message count, and achievement count.
+
+#### Scenario: Days together calculation
+- **WHEN** the user has an active couple relationship
+- **THEN** the system calculates days together from couple_relationship.created_at to current date
+
+#### Scenario: Memory count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of memory records for the couple
+
+#### Scenario: Location count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the count of distinct locations across all memory records for the couple
+
+#### Scenario: Message count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of chat messages exchanged between the couple
+
+#### Scenario: Achievement count
+- **WHEN** the user requests home stats
+- **THEN** the response includes the total count of unlocked achievements for the couple
+
+### Requirement: Upcoming anniversary section
+The response SHALL include a list of upcoming anniversaries sorted by nearest date.
+
+#### Scenario: Anniversary within 30 days
+- **WHEN** there is an anniversary occurring within 30 days
+- **THEN** the response includes the anniversary title and remaining days
+
+#### Scenario: No upcoming anniversary
+- **WHEN** there are no anniversaries within the upcoming window
+- **THEN** the response includes an empty list for upcoming anniversaries
+
+### Requirement: Recent memories timeline
+The response SHALL include recent memory records in reverse chronological order.
+
+#### Scenario: Recent memories with pagination
+- **WHEN** the user requests home stats
+- **THEN** the response includes the most recent 5 memory records with title, description snippet, date, and mood
+
+#### Scenario: Empty memory timeline
+- **WHEN** the couple has no memory records
+- **THEN** the response includes an empty list for recent memories
+
+### Requirement: Service layer uses mock data
+The AppService implementation SHALL return statically constructed data that matches the response schema.
+
+#### Scenario: Mock data consistency
+- **WHEN** the home stats endpoint is called
+- **THEN** the response structure and data types SHALL match the production schema exactly, with only the data values being mock
+
```

### `6ad2f44f` feat(android): 实现首页 UI、Token 自动刷新与导航

- **时间:** 2026-05-16 00:49:17 +0800

**提交信息:**

feat(android): 实现首页 UI、Token 自动刷新与导航

- 首页：统计卡片网格、纪念日区域、时间线列表、Pull-to-Refresh
- 数据层：HomeApi、HomeRepository、Hilt DI 模块、Domain Model
- ViewModel：HomeUiState/UiEvent 状态管理
- 认证增强：AuthApi 新增 logout、AuthNavigator SharedFlow buffer 修复
- 导航：5-Tab 底部导航，未实现 Tab 显示 Toast
- 依赖：新增 accompanist-swiperefresh

**代码变更:**

```diff
diff --git a/src/app/app/build.gradle.kts b/src/app/app/build.gradle.kts
index 1dc1085..3f5b361 100644
--- a/src/app/app/build.gradle.kts
+++ b/src/app/app/build.gradle.kts
@@ -97,6 +97,7 @@ dependencies {
 
     // Accompanist
     implementation(libs.accompanist.permissions)
+    implementation(libs.accompanist.swiperefresh)
 
     // Vico
     implementation(libs.vico.compose)
diff --git a/src/app/app/src/main/java/cn/iven/app/MainActivity.kt b/src/app/app/src/main/java/cn/iven/app/MainActivity.kt
index 0747014..eff129e 100644
--- a/src/app/app/src/main/java/cn/iven/app/MainActivity.kt
+++ b/src/app/app/src/main/java/cn/iven/app/MainActivity.kt
@@ -71,9 +71,18 @@ class MainActivity : ComponentActivity() {
 
                     LaunchedEffect(Unit) {
                         authNavigator.logoutEvent.collect {
+                            val refreshToken = sessionStorage.getRefreshToken()
+                            if (refreshToken != null) {
+                                try {
+                                    authApi.logout(cn.iven.app.core.network.LogoutRequest(refreshToken))
+                                } catch (_: Exception) {
+                                    // 后端登出失败也继续清本地态
+                                }
+                            }
                             sessionStorage.clear()
-                            navController.navigate(Routes.AUTH) {
-                                popUpTo(0) { inclusive = true }
+                            navController.navigate(Routes.LOGIN) {
+                                popUpTo(navController.graph.id) { inclusive = true }
+                                launchSingleTop = true
                             }
                         }
                     }
@@ -126,5 +135,6 @@ class MainActivity : ComponentActivity() {
         runOnUiThread {
             Toast.makeText(this, "登录已过期，请重新登录", Toast.LENGTH_SHORT).show()
         }
+        authNavigator.logout()
     }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/core/network/AuthApi.kt b/src/app/app/src/main/java/cn/iven/app/core/network/AuthApi.kt
index 7572b18..a58bd38 100644
--- a/src/app/app/src/main/java/cn/iven/app/core/network/AuthApi.kt
+++ b/src/app/app/src/main/java/cn/iven/app/core/network/AuthApi.kt
@@ -17,8 +17,18 @@ interface AuthApi {
     /** 使用 Refresh Token 换取新的 Access Token */
     @POST("api/v1/auth/refresh")
     suspend fun refresh(@Body request: RefreshRequest): ApiResponse<AuthResponseDto>
+
+    /** 使用 Refresh Token 注销登录态 */
+    @POST("api/v1/auth/logout")
+    suspend fun logout(@Body request: LogoutRequest): ApiResponse<Unit>
 }
 
+/** 登出请求体 */
+@Serializable
+data class LogoutRequest(
+    val refreshToken: String
+)
+
 /** Token 刷新请求体 */
 @Serializable
 data class RefreshRequest(
diff --git a/src/app/app/src/main/java/cn/iven/app/core/network/AuthNavigator.kt b/src/app/app/src/main/java/cn/iven/app/core/network/AuthNavigator.kt
index 30b89a4..30de45a 100644
--- a/src/app/app/src/main/java/cn/iven/app/core/network/AuthNavigator.kt
+++ b/src/app/app/src/main/java/cn/iven/app/core/network/AuthNavigator.kt
@@ -14,7 +14,7 @@ import javax.inject.Singleton
 @Singleton
 class AuthNavigator @Inject constructor() {
 
-    private val _logoutEvent = MutableSharedFlow<Unit>()
+    private val _logoutEvent = MutableSharedFlow<Unit>(extraBufferCapacity = 1)
 
     /** 全局登出事件流，[MainActivity] 订阅此流处理跳转 */
     val logoutEvent = _logoutEvent.asSharedFlow()
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/data/remote/HomeApi.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/data/remote/HomeApi.kt
new file mode 100644
index 0000000..14c2304
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/data/remote/HomeApi.kt
@@ -0,0 +1,46 @@
+/**
+ * 首页数据层 Retrofit 接口
+ *
+ * 提供首页统计数据查询接口。
+ */
+package cn.iven.app.feature.home.data.remote
+
+import cn.iven.app.core.network.ApiResponse
+import kotlinx.serialization.Serializable
+import retrofit2.http.GET
+
+interface HomeApi {
+
+    /** 获取首页统计数据 */
+    @GET("api/v1/home/stats")
+    suspend fun getHomeStats(): ApiResponse<HomeStatsDto>
+}
+
+/** 首页统计数据 DTO */
+@Serializable
+data class HomeStatsDto(
+    val daysTogether: Int,
+    val memoryCount: Int,
+    val locationCount: Int,
+    val messageCount: Int,
+    val achievementCount: Int,
+    val upcomingAnniversaries: List<AnniversaryCardDto>,
+    val recentMemories: List<MemoryTimelineItemDto>
+)
+
+/** 纪念日卡片 DTO */
+@Serializable
+data class AnniversaryCardDto(
+    val title: String,
+    val remainingDays: Int
+)
+
+/** 时间线记录项 DTO */
+@Serializable
+data class MemoryTimelineItemDto(
+    val id: Long,
+    val title: String,
+    val description: String,
+    val date: String,
+    val mood: Int
+)
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/data/repository/HomeRepositoryImpl.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/data/repository/HomeRepositoryImpl.kt
new file mode 100644
index 0000000..115ca67
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/data/repository/HomeRepositoryImpl.kt
@@ -0,0 +1,65 @@
+/**
+ * 首页仓库实现
+ *
+ * 负责调用远程首页接口并将 DTO 转换为领域层模型。
+ */
+package cn.iven.app.feature.home.data.repository
+
+import cn.iven.app.feature.home.data.remote.AnniversaryCardDto
+import cn.iven.app.feature.home.data.remote.HomeApi
+import cn.iven.app.feature.home.data.remote.HomeStatsDto
+import cn.iven.app.feature.home.data.remote.MemoryTimelineItemDto
+import cn.iven.app.feature.home.domain.HomeRepository
+import cn.iven.app.feature.home.domain.model.AnniversaryCard
+import cn.iven.app.feature.home.domain.model.HomeStats
+import cn.iven.app.feature.home.domain.model.MemoryTimelineItem
+import cn.iven.app.feature.home.domain.model.StatsCard
+import cn.iven.app.feature.home.domain.model.StatsCardType
+import javax.inject.Inject
+
+class HomeRepositoryImpl @Inject constructor(
+    private val api: HomeApi
+) : HomeRepository {
+
+    override suspend fun getHomeStats(): Result<HomeStats> {
+        return try {
+            val response = api.getHomeStats()
+            if (response.isSuccess && response.data != null) {
+                Result.success(response.data.toHomeStats())
+            } else {
+                Result.failure(Exception(response.message))
+            }
+        } catch (e: Exception) {
+            Result.failure(e)
+        }
+    }
+
+    /** 将远程 DTO 转换为领域层 HomeStats */
+    private fun HomeStatsDto.toHomeStats(): HomeStats {
+        return HomeStats(
+            statsCards = listOf(
+                StatsCard(StatsCardType.DAYS_TOGETHER, daysTogether, StatsCardType.DAYS_TOGETHER.label, StatsCardType.DAYS_TOGETHER.color),
+                StatsCard(StatsCardType.MEMORY_COUNT, memoryCount, StatsCardType.MEMORY_COUNT.label, StatsCardType.MEMORY_COUNT.color),
+                StatsCard(StatsCardType.LOCATION_COUNT, locationCount, StatsCardType.LOCATION_COUNT.label, StatsCardType.LOCATION_COUNT.color),
+                StatsCard(StatsCardType.MESSAGE_COUNT, messageCount, StatsCardType.MESSAGE_COUNT.label, StatsCardType.MESSAGE_COUNT.color),
+                StatsCard(StatsCardType.ACHIEVEMENT_COUNT, achievementCount, StatsCardType.ACHIEVEMENT_COUNT.label, StatsCardType.ACHIEVEMENT_COUNT.color)
+            ),
+            upcomingAnniversary = upcomingAnniversaries.firstOrNull()?.toAnniversaryCard(),
+            recentMemories = recentMemories.map { it.toMemoryTimelineItem() }
+        )
+    }
+
+    private fun AnniversaryCardDto.toAnniversaryCard(): AnniversaryCard {
+        return AnniversaryCard(title = title, remainingDays = remainingDays)
+    }
+
+    private fun MemoryTimelineItemDto.toMemoryTimelineItem(): MemoryTimelineItem {
+        return MemoryTimelineItem(
+            id = id,
+            title = title,
+            description = description,
+            date = date,
+            mood = mood
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/di/HomeModule.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/di/HomeModule.kt
new file mode 100644
index 0000000..554464a
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/di/HomeModule.kt
@@ -0,0 +1,37 @@
+/**
+ * 首页模块依赖注入配置
+ *
+ * 绑定首页仓库接口实现，并提供首页 Retrofit API 实例。
+ */
+package cn.iven.app.feature.home.di
+
+import cn.iven.app.feature.home.data.remote.HomeApi
+import cn.iven.app.feature.home.data.repository.HomeRepositoryImpl
+import cn.iven.app.feature.home.domain.HomeRepository
+import dagger.Binds
+import dagger.Module
+import dagger.Provides
+import dagger.hilt.InstallIn
+import dagger.hilt.components.SingletonComponent
+import retrofit2.Retrofit
+import javax.inject.Singleton
+
+@Module
+@InstallIn(SingletonComponent::class)
+abstract class HomeModule {
+
+    /** 绑定 HomeRepository 接口到 HomeRepositoryImpl 实现 */
+    @Binds
+    @Singleton
+    abstract fun bindHomeRepository(impl: HomeRepositoryImpl): HomeRepository
+
+    companion object {
+
+        /** 提供首页 Retrofit API */
+        @Provides
+        @Singleton
+        fun provideHomeApi(retrofit: Retrofit): HomeApi {
+            return retrofit.create(HomeApi::class.java)
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/domain/HomeRepository.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/domain/HomeRepository.kt
new file mode 100644
index 0000000..31feef3
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/domain/HomeRepository.kt
@@ -0,0 +1,14 @@
+/**
+ * 首页仓库接口
+ *
+ * 定义首页数据操作的领域层契约。
+ */
+package cn.iven.app.feature.home.domain
+
+import cn.iven.app.feature.home.domain.model.HomeStats
+
+interface HomeRepository {
+
+    /** 获取首页统计数据 */
+    suspend fun getHomeStats(): Result<HomeStats>
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/domain/model/HomeStats.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/domain/model/HomeStats.kt
new file mode 100644
index 0000000..1b7e99d
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/domain/model/HomeStats.kt
@@ -0,0 +1,54 @@
+/**
+ * 首页领域层模型
+ *
+ * 定义首页展示所需的领域对象，包含统计卡片、纪念日和最近记录。
+ */
+package cn.iven.app.feature.home.domain.model
+
+import androidx.compose.ui.graphics.Color
+import cn.iven.app.ui.theme.FreshGreen
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.RomanticPurple
+import cn.iven.app.ui.theme.WarmOrange
+
+/** 首页完整统计数据 */
+data class HomeStats(
+    val statsCards: List<StatsCard>,
+    val upcomingAnniversary: AnniversaryCard?,
+    val recentMemories: List<MemoryTimelineItem>
+)
+
+/** 统计卡片 */
+data class StatsCard(
+    val type: StatsCardType,
+    val value: Int,
+    val label: String,
+    val color: Color
+)
+
+/** 统计卡片类型枚举，每种类型对应固定颜色和标签 */
+enum class StatsCardType(
+    val label: String,
+    val color: Color
+) {
+    DAYS_TOGETHER("在一起", LovePink),
+    MEMORY_COUNT("记录", RomanticPurple),
+    LOCATION_COUNT("地点", WarmOrange),
+    MESSAGE_COUNT("消息", FreshGreen),
+    ACHIEVEMENT_COUNT("成就", LovePink)
+}
+
+/** 纪念日卡片 */
+data class AnniversaryCard(
+    val title: String,
+    val remainingDays: Int
+)
+
+/** 时间线记录项 */
+data class MemoryTimelineItem(
+    val id: Long,
+    val title: String,
+    val description: String,
+    val date: String,
+    val mood: Int
+)
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
index 7d66a4f..00ad6ca 100644
--- a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeScreen.kt
@@ -1,33 +1,211 @@
 /**
  * 首页
  *
- * 应用主页面，展示情侣共同内容。当前为占位实现。
+ * 应用主页面，展示情侣统计数据、纪念日和最近记录。
+ * 支持下拉刷新和底部导航栏交互。
  */
 package cn.iven.app.feature.home.ui
 
+import androidx.compose.foundation.background
+import androidx.compose.foundation.clickable
+import androidx.compose.foundation.layout.Arrangement
 import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
 import androidx.compose.foundation.layout.fillMaxSize
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.rememberScrollState
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.foundation.verticalScroll
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.filled.Notifications
+import androidx.compose.material3.CircularProgressIndicator
+import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.Icon
+import androidx.compose.material3.IconButton
+import androidx.compose.material3.Scaffold
 import androidx.compose.material3.Text
+import androidx.compose.material3.TopAppBar
+import androidx.compose.material3.TopAppBarDefaults
 import androidx.compose.runtime.Composable
+import androidx.compose.runtime.getValue
 import androidx.compose.ui.Alignment
 import androidx.compose.ui.Modifier
+import androidx.compose.ui.text.font.FontWeight
 import androidx.compose.ui.tooling.preview.Preview
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import androidx.hilt.navigation.compose.hiltViewModel
+import androidx.lifecycle.compose.collectAsStateWithLifecycle
+import cn.iven.app.feature.home.domain.model.AnniversaryCard
+import cn.iven.app.feature.home.domain.model.MemoryTimelineItem
+import cn.iven.app.feature.home.domain.model.StatsCard
+import cn.iven.app.feature.home.domain.model.StatsCardType
+import cn.iven.app.feature.home.ui.components.RecentMemoriesSection
+import cn.iven.app.feature.home.ui.components.StatsCardsSection
+import cn.iven.app.feature.home.ui.components.UpcomingAnniversarySection
+import cn.iven.app.ui.theme.BackgroundLight
 import cn.iven.app.ui.theme.LianjiTheme
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import com.google.accompanist.swiperefresh.SwipeRefresh
+import com.google.accompanist.swiperefresh.SwipeRefreshIndicator
+import com.google.accompanist.swiperefresh.rememberSwipeRefreshState
 
+@OptIn(ExperimentalMaterial3Api::class)
 @Composable
-fun HomeScreen() {
+fun HomeScreen(
+    modifier: Modifier = Modifier,
+    viewModel: HomeViewModel = hiltViewModel()
+) {
+    val uiState by viewModel.uiState.collectAsStateWithLifecycle()
+    val isRefreshing = uiState is HomeUiState.Loading
+    val swipeRefreshState = rememberSwipeRefreshState(isRefreshing)
+
+    Scaffold(
+        modifier = modifier,
+        topBar = {
+            TopAppBar(
+                title = {
+                    Text(
+                        text = "恋记",
+                        fontSize = 20.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
+                    )
+                },
+                actions = {
+                    IconButton(onClick = { /* TODO: 通知页面 */ }) {
+                        Icon(
+                            imageVector = Icons.Default.Notifications,
+                            contentDescription = "通知",
+                            tint = TextPrimaryLight
+                        )
+                    }
+                },
+                colors = TopAppBarDefaults.topAppBarColors(
+                    containerColor = BackgroundLight
+                )
+            )
+        }
+    ) { paddingValues ->
+        SwipeRefresh(
+            state = swipeRefreshState,
+            onRefresh = { viewModel.onEvent(HomeUiEvent.Refresh) },
+            modifier = Modifier.padding(paddingValues),
+            indicator = { state, trigger ->
+                SwipeRefreshIndicator(
+                    state = state,
+                    refreshTriggerDistance = trigger,
+                    contentColor = LovePink
+                )
+            }
+        ) {
+            when (val state = uiState) {
+                is HomeUiState.Loading -> {
+                    Box(
+                        modifier = Modifier.fillMaxSize(),
+                        contentAlignment = Alignment.Center
+                    ) {
+                        CircularProgressIndicator(color = LovePink)
+                    }
+                }
+                is HomeUiState.Error -> {
+                    ErrorState(
+                        message = state.message,
+                        onRetry = { viewModel.onEvent(HomeUiEvent.Retry) }
+                    )
+                }
+                is HomeUiState.Success -> {
+                    HomeContent(
+                        statsCards = state.statsCards,
+                        upcomingAnniversary = state.upcomingAnniversary,
+                        recentMemories = state.recentMemories
+                    )
+                }
+            }
+        }
+    }
+}
+
+@Composable
+private fun HomeContent(
+    statsCards: List<StatsCard>,
+    upcomingAnniversary: AnniversaryCard?,
+    recentMemories: List<MemoryTimelineItem>,
+    modifier: Modifier = Modifier
+) {
+    Column(
+        modifier = modifier
+            .fillMaxSize()
+            .background(BackgroundLight)
+            .verticalScroll(rememberScrollState())
+            .padding(16.dp),
+        verticalArrangement = Arrangement.spacedBy(24.dp)
+    ) {
+        StatsCardsSection(statsCards = statsCards)
+        UpcomingAnniversarySection(anniversary = upcomingAnniversary)
+        RecentMemoriesSection(memories = recentMemories)
+    }
+}
+
+@Composable
+private fun ErrorState(
+    message: String,
+    onRetry: () -> Unit,
+    modifier: Modifier = Modifier
+) {
     Box(
-        modifier = Modifier.fillMaxSize(),
+        modifier = modifier.fillMaxSize(),
         contentAlignment = Alignment.Center
     ) {
-        Text("Home Screen")
+        Column(
+            horizontalAlignment = Alignment.CenterHorizontally,
+            verticalArrangement = Arrangement.spacedBy(16.dp)
+        ) {
+            Text(
+                text = message,
+                fontSize = 14.sp,
+                color = TextPrimaryLight
+            )
+            Box(
+                modifier = Modifier
+                    .fillMaxWidth(0.5f)
+                    .padding(horizontal = 32.dp)
+                    .background(LovePink, RoundedCornerShape(12.dp))
+                    .clickable { onRetry() }
+                    .padding(vertical = 12.dp),
+                contentAlignment = Alignment.Center
+            ) {
+                Text(
+                    text = "重试",
+                    fontSize = 16.sp,
+                    fontWeight = FontWeight.SemiBold,
+                    color = SurfaceLight
+                )
+            }
+        }
     }
 }
 
-@Preview(showBackground = true, name = "Home")
+@Preview(showBackground = true, name = "Home Success")
 @Composable
 private fun HomeScreenPreview() {
     LianjiTheme {
-        HomeScreen()
+        HomeContent(
+            statsCards = listOf(
+                StatsCard(StatsCardType.DAYS_TOGETHER, 365, "在一起", StatsCardType.DAYS_TOGETHER.color),
+                StatsCard(StatsCardType.MEMORY_COUNT, 42, "记录", StatsCardType.MEMORY_COUNT.color),
+                StatsCard(StatsCardType.LOCATION_COUNT, 8, "地点", StatsCardType.LOCATION_COUNT.color),
+                StatsCard(StatsCardType.MESSAGE_COUNT, 128, "消息", StatsCardType.MESSAGE_COUNT.color),
+                StatsCard(StatsCardType.ACHIEVEMENT_COUNT, 5, "成就", StatsCardType.ACHIEVEMENT_COUNT.color)
+            ),
+            upcomingAnniversary = AnniversaryCard("100天纪念日", 23),
+            recentMemories = listOf(
+                MemoryTimelineItem(1, "第一次看电影", "看了《你的名字》", "2024-01-15", 1),
+                MemoryTimelineItem(2, "周末野餐", "在公园度过美好下午", "2024-01-10", 4)
+            )
+        )
     }
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiEvent.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiEvent.kt
new file mode 100644
index 0000000..6a61f16
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiEvent.kt
@@ -0,0 +1,9 @@
+/**
+ * 首页 UI 事件定义
+ */
+package cn.iven.app.feature.home.ui
+
+sealed interface HomeUiEvent {
+    data object Refresh : HomeUiEvent
+    data object Retry : HomeUiEvent
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiState.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiState.kt
new file mode 100644
index 0000000..7effccd
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeUiState.kt
@@ -0,0 +1,18 @@
+/**
+ * 首页 UI 状态定义
+ */
+package cn.iven.app.feature.home.ui
+
+import cn.iven.app.feature.home.domain.model.AnniversaryCard
+import cn.iven.app.feature.home.domain.model.MemoryTimelineItem
+import cn.iven.app.feature.home.domain.model.StatsCard
+
+sealed interface HomeUiState {
+    data object Loading : HomeUiState
+    data class Success(
+        val statsCards: List<StatsCard>,
+        val upcomingAnniversary: AnniversaryCard?,
+        val recentMemories: List<MemoryTimelineItem>
+    ) : HomeUiState
+    data class Error(val message: String) : HomeUiState
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt
new file mode 100644
index 0000000..e19ff1f
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/HomeViewModel.kt
@@ -0,0 +1,74 @@
+/**
+ * 首页 ViewModel
+ *
+ * 管理首页数据加载和 UI 状态。
+ */
+package cn.iven.app.feature.home.ui
+
+import androidx.lifecycle.ViewModel
+import androidx.lifecycle.viewModelScope
+import cn.iven.app.feature.home.domain.HomeRepository
+import dagger.hilt.android.lifecycle.HiltViewModel
+import kotlinx.coroutines.flow.MutableStateFlow
+import kotlinx.coroutines.flow.StateFlow
+import kotlinx.coroutines.flow.asStateFlow
+import kotlinx.coroutines.launch
+import javax.inject.Inject
+
+@HiltViewModel
+class HomeViewModel @Inject constructor(
+    private val repository: HomeRepository
+) : ViewModel() {
+
+    private val _uiState = MutableStateFlow<HomeUiState>(HomeUiState.Loading)
+
+    /** 首页 UI 状态流 */
+    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()
+
+    init {
+        loadStats()
+    }
+
+    /** 处理 UI 事件 */
+    fun onEvent(event: HomeUiEvent) {
+        when (event) {
+            is HomeUiEvent.Refresh -> refresh()
+            is HomeUiEvent.Retry -> loadStats()
+        }
+    }
+
+    /** 加载首页统计数据 */
+    private fun loadStats() {
+        viewModelScope.launch {
+            _uiState.value = HomeUiState.Loading
+            val result = repository.getHomeStats()
+            _uiState.value = if (result.isSuccess) {
+                val stats = result.getOrThrow()
+                HomeUiState.Success(
+                    statsCards = stats.statsCards,
+                    upcomingAnniversary = stats.upcomingAnniversary,
+                    recentMemories = stats.recentMemories
+                )
+            } else {
+                HomeUiState.Error(result.exceptionOrNull()?.message ?: "加载失败")
+            }
+        }
+    }
+
+    /** 刷新首页数据（用于下拉刷新） */
+    private fun refresh() {
+        viewModelScope.launch {
+            val result = repository.getHomeStats()
+            _uiState.value = if (result.isSuccess) {
+                val stats = result.getOrThrow()
+                HomeUiState.Success(
+                    statsCards = stats.statsCards,
+                    upcomingAnniversary = stats.upcomingAnniversary,
+                    recentMemories = stats.recentMemories
+                )
+            } else {
+                HomeUiState.Error(result.exceptionOrNull()?.message ?: "刷新失败")
+            }
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/RecentMemoriesSection.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/RecentMemoriesSection.kt
new file mode 100644
index 0000000..7e98655
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/RecentMemoriesSection.kt
@@ -0,0 +1,163 @@
+/**
+ * 最近记录时间线区域
+ *
+ * 展示最近的心情记录时间线，包含标题行和时间线条目列表。
+ */
+package cn.iven.app.feature.home.ui.components
+
+import androidx.compose.foundation.background
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
+import androidx.compose.foundation.layout.width
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material3.Card
+import androidx.compose.material3.CardDefaults
+import androidx.compose.material3.Text
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.feature.home.domain.model.MemoryTimelineItem
+import cn.iven.app.ui.theme.FreshGreen
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
+import cn.iven.app.ui.theme.RomanticPurple
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextBodyLight
+import cn.iven.app.ui.theme.TextDisabledLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import cn.iven.app.ui.theme.TextSecondaryLight
+import cn.iven.app.ui.theme.SkyBlue
+import cn.iven.app.ui.theme.WarmOrange
+
+/** Mood 颜色映射：1=粉色, 2=紫色, 3=橙色, 4=绿色, 5=蓝色 */
+private fun moodColor(mood: Int) = when (mood) {
+    1 -> LovePink
+    2 -> RomanticPurple
+    3 -> WarmOrange
+    4 -> FreshGreen
+    else -> SkyBlue
+}
+
+@Composable
+fun RecentMemoriesSection(
+    memories: List<MemoryTimelineItem>,
+    modifier: Modifier = Modifier
+) {
+    Column(
+        modifier = modifier.fillMaxWidth(),
+        verticalArrangement = Arrangement.spacedBy(12.dp)
+    ) {
+        // 标题行
+        Row(
+            modifier = Modifier.fillMaxWidth(),
+            horizontalArrangement = Arrangement.SpaceBetween,
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            Text(
+                text = "最近记录",
+                fontSize = 16.sp,
+                fontWeight = FontWeight.SemiBold,
+                color = TextPrimaryLight
+            )
+            Text(
+                text = "查看全部",
+                fontSize = 13.sp,
+                fontWeight = FontWeight.Medium,
+                color = LovePink
+            )
+        }
+
+        // 时间线列表
+        if (memories.isEmpty()) {
+            EmptyMemoriesState()
+        } else {
+            Column(
+                verticalArrangement = Arrangement.spacedBy(8.dp)
+            ) {
+                memories.forEach { memory ->
+                    MemoryTimelineItemCard(memory = memory)
+                }
+            }
+        }
+    }
+}
+
+@Composable
+private fun MemoryTimelineItemCard(
+    memory: MemoryTimelineItem,
+    modifier: Modifier = Modifier
+) {
+    Card(
+        modifier = modifier.fillMaxWidth(),
+        colors = CardDefaults.cardColors(containerColor = SurfaceLight),
+        shape = RoundedCornerShape(12.dp)
+    ) {
+        Row(
+            modifier = Modifier
+                .fillMaxWidth()
+                .padding(16.dp),
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            // Mood 颜色圆点
+            Box(
+                modifier = Modifier
+                    .size(10.dp)
+                    .clip(RoundedCornerShape(5.dp))
+                    .background(moodColor(memory.mood))
+            )
+
+            Spacer(modifier = Modifier.width(12.dp))
+
+            // 内容
+            Column(
+                verticalArrangement = Arrangement.spacedBy(2.dp)
+            ) {
+                Text(
+                    text = memory.title,
+                    fontSize = 14.sp,
+                    fontWeight = FontWeight.Medium,
+                    color = TextPrimaryLight
+                )
+                Text(
+                    text = memory.description,
+                    fontSize = 12.sp,
+                    color = TextBodyLight,
+                    maxLines = 1
+                )
+                Text(
+                    text = memory.date,
+                    fontSize = 11.sp,
+                    color = TextSecondaryLight
+                )
+            }
+        }
+    }
+}
+
+@Composable
+private fun EmptyMemoriesState(
+    modifier: Modifier = Modifier
+) {
+    Box(
+        modifier = modifier
+            .fillMaxWidth()
+            .padding(vertical = 32.dp),
+        contentAlignment = Alignment.Center
+    ) {
+        Text(
+            text = "还没有记录，快去添加第一条吧~",
+            fontSize = 14.sp,
+            color = TextDisabledLight
+        )
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/StatsCardsSection.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/StatsCardsSection.kt
new file mode 100644
index 0000000..3ee0060
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/StatsCardsSection.kt
@@ -0,0 +1,79 @@
+/**
+ * 统计卡片区域
+ *
+ * 3+2 网格布局展示5个统计卡片，每个卡片有对应的颜色主题。
+ */
+package cn.iven.app.feature.home.ui.components
+
+import androidx.compose.foundation.background
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.ExperimentalLayoutApi
+import androidx.compose.foundation.layout.FlowRow
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.height
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.width
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material3.Text
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.feature.home.domain.model.StatsCard
+import cn.iven.app.ui.theme.SurfaceLight
+
+@OptIn(ExperimentalLayoutApi::class)
+@Composable
+fun StatsCardsSection(
+    statsCards: List<StatsCard>,
+    modifier: Modifier = Modifier
+) {
+    FlowRow(
+        modifier = modifier.fillMaxWidth(),
+        horizontalArrangement = Arrangement.spacedBy(12.dp, Alignment.CenterHorizontally),
+        verticalArrangement = Arrangement.spacedBy(12.dp),
+        maxItemsInEachRow = 3
+    ) {
+        statsCards.forEach { card ->
+            StatsCardItem(card = card)
+        }
+    }
+}
+
+@Composable
+private fun StatsCardItem(
+    card: StatsCard,
+    modifier: Modifier = Modifier
+) {
+    Box(
+        modifier = modifier
+            .width(100.dp)
+            .height(80.dp)
+            .clip(RoundedCornerShape(12.dp))
+            .background(card.color),
+        contentAlignment = Alignment.Center
+    ) {
+        Column(
+            horizontalAlignment = Alignment.CenterHorizontally,
+            verticalArrangement = Arrangement.spacedBy(4.dp)
+        ) {
+            Text(
+                text = card.value.toString(),
+                fontSize = 20.sp,
+                fontWeight = FontWeight.Bold,
+                color = SurfaceLight
+            )
+            Text(
+                text = card.label,
+                fontSize = 11.sp,
+                fontWeight = FontWeight.Medium,
+                color = SurfaceLight
+            )
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt
new file mode 100644
index 0000000..f50df46
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/home/ui/components/UpcomingAnniversarySection.kt
@@ -0,0 +1,130 @@
+/**
+ * 即将到来纪念日区域
+ *
+ * 展示最近的纪念日卡片，包含标题行和卡片内容。
+ */
+package cn.iven.app.feature.home.ui.components
+
+import androidx.compose.foundation.background
+import androidx.compose.foundation.layout.Arrangement
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.Column
+import androidx.compose.foundation.layout.Row
+import androidx.compose.foundation.layout.Spacer
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.layout.size
+import androidx.compose.foundation.layout.width
+import androidx.compose.foundation.shape.CircleShape
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.filled.Cake
+import androidx.compose.material3.Card
+import androidx.compose.material3.CardDefaults
+import androidx.compose.material3.Icon
+import androidx.compose.material3.Text
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.draw.clip
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import cn.iven.app.feature.home.domain.model.AnniversaryCard
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.LovePinkLight
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import cn.iven.app.ui.theme.TextSecondaryLight
+import cn.iven.app.ui.theme.WarmOrange
+
+@Composable
+fun UpcomingAnniversarySection(
+    anniversary: AnniversaryCard?,
+    modifier: Modifier = Modifier
+) {
+    Column(
+        modifier = modifier.fillMaxWidth(),
+        verticalArrangement = Arrangement.spacedBy(12.dp)
+    ) {
+        // 标题行
+        Row(
+            modifier = Modifier.fillMaxWidth(),
+            horizontalArrangement = Arrangement.SpaceBetween,
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            Text(
+                text = "即将到来",
+                fontSize = 16.sp,
+                fontWeight = FontWeight.SemiBold,
+                color = TextPrimaryLight
+            )
+            Text(
+                text = "查看全部",
+                fontSize = 13.sp,
+                fontWeight = FontWeight.Medium,
+                color = LovePink
+            )
+        }
+
+        // 纪念日卡片
+        if (anniversary != null) {
+            AnniversaryCardItem(anniversary = anniversary)
+        }
+    }
+}
+
+@Composable
+private fun AnniversaryCardItem(
+    anniversary: AnniversaryCard,
+    modifier: Modifier = Modifier
+) {
+    Card(
+        modifier = modifier.fillMaxWidth(),
+        colors = CardDefaults.cardColors(containerColor = SurfaceLight),
+        shape = RoundedCornerShape(12.dp)
+    ) {
+        Row(
+            modifier = Modifier
+                .fillMaxWidth()
+                .padding(16.dp),
+            verticalAlignment = Alignment.CenterVertically
+        ) {
+            // 蛋糕图标
+            Box(
+                modifier = Modifier
+                    .size(40.dp)
+                    .clip(CircleShape)
+                    .background(LovePinkLight),
+                contentAlignment = Alignment.Center
+            ) {
+                Icon(
+                    imageVector = Icons.Default.Cake,
+                    contentDescription = null,
+                    modifier = Modifier.size(20.dp),
+                    tint = LovePink
+                )
+            }
+
+            Spacer(modifier = Modifier.width(12.dp))
+
+            // 标题和天数
+            Column(
+                verticalArrangement = Arrangement.spacedBy(2.dp)
+            ) {
+                Text(
+                    text = anniversary.title,
+                    fontSize = 14.sp,
+                    fontWeight = FontWeight.Medium,
+                    color = TextPrimaryLight
+                )
+                Text(
+                    text = "还有 ${anniversary.remainingDays} 天",
+                    fontSize = 13.sp,
+                    fontWeight = FontWeight.Medium,
+                    color = WarmOrange
+                )
+            }
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt b/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt
new file mode 100644
index 0000000..788182f
--- /dev/null
+++ b/src/app/app/src/main/java/cn/iven/app/feature/profile/ui/ProfileScreen.kt
@@ -0,0 +1,85 @@
+package cn.iven.app.feature.profile.ui
+
+import androidx.compose.foundation.layout.Box
+import androidx.compose.foundation.layout.fillMaxSize
+import androidx.compose.foundation.layout.fillMaxWidth
+import androidx.compose.foundation.layout.padding
+import androidx.compose.foundation.shape.RoundedCornerShape
+import androidx.compose.material3.Button
+import androidx.compose.material3.ButtonDefaults
+import androidx.compose.material3.ExperimentalMaterial3Api
+import androidx.compose.material3.Scaffold
+import androidx.compose.material3.Text
+import androidx.compose.material3.TopAppBar
+import androidx.compose.material3.TopAppBarDefaults
+import androidx.compose.runtime.Composable
+import androidx.compose.ui.Alignment
+import androidx.compose.ui.Modifier
+import androidx.compose.ui.text.font.FontWeight
+import androidx.compose.ui.unit.dp
+import androidx.compose.ui.unit.sp
+import androidx.hilt.navigation.compose.hiltViewModel
+import cn.iven.app.core.network.AuthNavigator
+import cn.iven.app.ui.theme.BackgroundLight
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.SurfaceLight
+import cn.iven.app.ui.theme.TextPrimaryLight
+import androidx.lifecycle.ViewModel
+import dagger.hilt.android.lifecycle.HiltViewModel
+import javax.inject.Inject
+
+@HiltViewModel
+class ProfileViewModel @Inject constructor(
+    val authNavigator: AuthNavigator
+) : ViewModel()
+
+@OptIn(ExperimentalMaterial3Api::class)
+@Composable
+fun ProfileScreen(
+    modifier: Modifier = Modifier,
+    viewModel: ProfileViewModel = hiltViewModel()
+) {
+    Scaffold(
+        modifier = modifier,
+        topBar = {
+            TopAppBar(
+                title = {
+                    Text(
+                        text = "我的",
+                        fontSize = 20.sp,
+                        fontWeight = FontWeight.SemiBold,
+                        color = TextPrimaryLight
+                    )
+                },
+                colors = TopAppBarDefaults.topAppBarColors(
+                    containerColor = BackgroundLight
+                )
+            )
+        }
+    ) { paddingValues ->
+        Box(
+            modifier = Modifier
+                .fillMaxSize()
+                .padding(paddingValues)
+                .padding(16.dp),
+            contentAlignment = Alignment.BottomCenter
+        ) {
+            Button(
+                onClick = { viewModel.authNavigator.logout() },
+                modifier = Modifier.fillMaxWidth(),
+                shape = RoundedCornerShape(12.dp),
+                colors = ButtonDefaults.buttonColors(
+                    containerColor = LovePink,
+                    contentColor = SurfaceLight
+                )
+            ) {
+                Text(
+                    text = "退出登录",
+                    fontSize = 16.sp,
+                    fontWeight = FontWeight.SemiBold,
+                    modifier = Modifier.padding(vertical = 4.dp)
+                )
+            }
+        }
+    }
+}
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt b/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
index 632d18e..db2b43c 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/MainNavGraph.kt
@@ -5,8 +5,12 @@
  */
 package cn.iven.app.navigation
 
+import android.widget.Toast
 import androidx.compose.foundation.layout.padding
 import androidx.compose.material.icons.Icons
+import androidx.compose.material.icons.automirrored.filled.Chat
+import androidx.compose.material.icons.filled.Book
+import androidx.compose.material.icons.filled.CalendarToday
 import androidx.compose.material.icons.filled.Home
 import androidx.compose.material.icons.filled.Person
 import androidx.compose.material3.Icon
@@ -17,12 +21,31 @@ import androidx.compose.material3.Text
 import androidx.compose.runtime.Composable
 import androidx.compose.runtime.getValue
 import androidx.compose.ui.Modifier
+import androidx.compose.ui.platform.LocalContext
 import androidx.navigation.NavGraphBuilder
 import androidx.navigation.NavHostController
 import androidx.navigation.compose.composable
 import androidx.navigation.compose.currentBackStackEntryAsState
 import androidx.navigation.navigation
 import cn.iven.app.feature.home.ui.HomeScreen
+import cn.iven.app.feature.profile.ui.ProfileScreen
+import cn.iven.app.ui.theme.LovePink
+import cn.iven.app.ui.theme.TextSecondaryLight
+
+/** 底部导航项定义 */
+private data class BottomNavItem(
+    val route: String,
+    val label: String,
+    val icon: androidx.compose.ui.graphics.vector.ImageVector
+)
+
+private val bottomNavItems = listOf(
+    BottomNavItem(Routes.HOME, "首页", Icons.Default.Home),
+    BottomNavItem(Routes.NOTE, "记事", Icons.Default.Book),
+    BottomNavItem(Routes.ANNIVERSARY, "纪念日", Icons.Default.CalendarToday),
+    BottomNavItem(Routes.CHAT, "聊天", Icons.AutoMirrored.Filled.Chat),
+    BottomNavItem(Routes.PROFILE, "我的", Icons.Default.Person)
+)
 
 /** 构建主页面模块导航图 */
 fun NavGraphBuilder.mainNavGraph(
@@ -33,8 +56,13 @@ fun NavGraphBuilder.mainNavGraph(
         route = Routes.MAIN
     ) {
         composable(Routes.HOME) {
-            MainScaffold(navController = navController) {
-                HomeScreen()
+            MainScaffold(navController = navController) { modifier ->
+                HomeScreen(modifier = modifier)
+            }
+        }
+        composable(Routes.PROFILE) {
+            MainScaffold(navController = navController) { modifier ->
+                ProfileScreen(modifier = modifier)
             }
         }
     }
@@ -43,7 +71,7 @@ fun NavGraphBuilder.mainNavGraph(
 /**
  * 主页面 Scaffold 布局
  *
- * 包含底部导航栏（首页、我的），包裹主内容区域。
+ * 包含底部导航栏（首页、记事、纪念日、聊天、我的），包裹主内容区域。
  */
 @Composable
 private fun MainScaffold(
@@ -52,28 +80,43 @@ private fun MainScaffold(
 ) {
     val navBackStackEntry by navController.currentBackStackEntryAsState()
     val currentRoute = navBackStackEntry?.destination?.route
+    val context = LocalContext.current
 
     Scaffold(
         bottomBar = {
             NavigationBar {
-                NavigationBarItem(
-                    icon = { Icon(Icons.Default.Home, contentDescription = "首页") },
-                    label = { Text("首页") },
-                    selected = currentRoute == Routes.HOME,
-                    onClick = {
-                        if (currentRoute != Routes.HOME) {
-                            navController.navigate(Routes.HOME) {
-                                popUpTo(Routes.MAIN) { inclusive = false }
+                bottomNavItems.forEach { item ->
+                    val selected = currentRoute == item.route
+                    val isImplemented = item.route == Routes.HOME || item.route == Routes.PROFILE
+
+                    NavigationBarItem(
+                        icon = {
+                            Icon(
+                                imageVector = item.icon,
+                                contentDescription = item.label,
+                                tint = if (selected) LovePink else TextSecondaryLight
+                            )
+                        },
+                        label = {
+                            Text(
+                                text = item.label,
+                                color = if (selected) LovePink else TextSecondaryLight
+                            )
+                        },
+                        selected = selected,
+                        onClick = {
+                            if (isImplemented) {
+                                if (currentRoute != item.route) {
+                                    navController.navigate(item.route) {
+                                        popUpTo(Routes.MAIN) { inclusive = false }
+                                    }
+                                }
+                            } else {
+                                Toast.makeText(context, "功能开发中", Toast.LENGTH_SHORT).show()
                             }
                         }
-                    }
-                )
-                NavigationBarItem(
-                    icon = { Icon(Icons.Default.Person, contentDescription = "我的") },
-                    label = { Text("我的") },
-                    selected = false,
-                    onClick = { }
-                )
+                    )
+                }
             }
         }
     ) { innerPadding ->
diff --git a/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt b/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
index 0439cfe..b554305 100644
--- a/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
+++ b/src/app/app/src/main/java/cn/iven/app/navigation/Routes.kt
@@ -13,4 +13,8 @@ object Routes {
 
     const val MAIN = "main"
     const val HOME = "main/home"
+    const val NOTE = "main/note"
+    const val ANNIVERSARY = "main/anniversary"
+    const val CHAT = "main/chat"
+    const val PROFILE = "main/profile"
 }
diff --git a/src/app/app/src/main/java/cn/iven/app/ui/theme/Color.kt b/src/app/app/src/main/java/cn/iven/app/ui/theme/Color.kt
index c03c312..64eb5dd 100644
--- a/src/app/app/src/main/java/cn/iven/app/ui/theme/Color.kt
+++ b/src/app/app/src/main/java/cn/iven/app/ui/theme/Color.kt
@@ -25,6 +25,9 @@ val WarmOrange = Color(0xFFFFB347)
 /** 辅助色 - 清新绿 */
 val FreshGreen = Color(0xFF7FD8B8)
 
+/** 辅助色 - 天空蓝 */
+val SkyBlue = Color(0xFF6BB5FF)
+
 // --- 浅色主题 ---
 val BackgroundLight = Color(0xFFFAFAFA)
 val SurfaceLight = Color(0xFFFFFFFF)
diff --git a/src/app/gradle/libs.versions.toml b/src/app/gradle/libs.versions.toml
index 39c87ef..727470f 100644
--- a/src/app/gradle/libs.versions.toml
+++ b/src/app/gradle/libs.versions.toml
@@ -78,6 +78,7 @@ paging-compose = { group = "androidx.paging", name = "paging-compose", version.r
 
 # Accompanist
 accompanist-permissions = { group = "com.google.accompanist", name = "accompanist-permissions", version.ref = "accompanist" }
+accompanist-swiperefresh = { group = "com.google.accompanist", name = "accompanist-swiperefresh", version.ref = "accompanist" }
 
 # Vico
 vico-compose = { group = "com.patrykandpatrick.vico", name = "compose", version.ref = "vico" }
```

### `1257e0aa` feat(api): 实现首页统计 Mock API

- **时间:** 2026-05-16 00:48:41 +0800

**提交信息:**

feat(api): 实现首页统计 Mock API

- 新增 GET /api/v1/home/stats 接口
- 实现 HomeAppService 返回 Mock 数据（daysTogether 从真实关系创建时间计算）
- 定义 HomeStatsResponseDTO、AnniversaryCardDTO、MemoryTimelineItemDTO
- 新增 HomeAppServiceImpl 单元测试

**代码变更:**

```diff
diff --git a/src/api/src/main/java/cn/iven/lianji/api/controller/v1/home/HomeController.java b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/home/HomeController.java
new file mode 100644
index 0000000..4e9c58b
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/controller/v1/home/HomeController.java
@@ -0,0 +1,40 @@
+package cn.iven.lianji.api.controller.v1.home;
+
+import cn.iven.lianji.api.converter.home.HomeResponseConverter;
+import cn.iven.lianji.api.dto.home.HomeStatsResponseDTO;
+import cn.iven.lianji.application.HomeStatsResult;
+import cn.iven.lianji.application.service.HomeAppService;
+import lombok.RequiredArgsConstructor;
+import org.springframework.security.core.context.SecurityContextHolder;
+import org.springframework.web.bind.annotation.GetMapping;
+import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RestController;
+
+/**
+ * 首页接口（V1）。
+ * <p>提供首页统计数据查询能力。</p>
+ */
+@RestController
+@RequestMapping("/api/v1/home")
+@RequiredArgsConstructor
+public class HomeController {
+
+    private final HomeAppService homeAppService;
+    private final HomeResponseConverter responseConverter;
+
+    @GetMapping("/stats")
+    public HomeStatsResponseDTO getStats() {
+        Long userId = getCurrentUserId();
+        HomeStatsResult result = homeAppService.getStats(userId);
+        return responseConverter.toDTO(result);
+    }
+
+    /**
+     * 从 SecurityContext 获取当前登录用户 ID。
+     * <p>JWT 过滤器将 userId 写入 username 字段。</p>
+     */
+    private Long getCurrentUserId() {
+        String username = SecurityContextHolder.getContext().getAuthentication().getName();
+        return Long.valueOf(username);
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/converter/home/HomeResponseConverter.java b/src/api/src/main/java/cn/iven/lianji/api/converter/home/HomeResponseConverter.java
new file mode 100644
index 0000000..82cd619
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/converter/home/HomeResponseConverter.java
@@ -0,0 +1,75 @@
+package cn.iven.lianji.api.converter.home;
+
+import cn.iven.lianji.api.dto.home.AnniversaryCardDTO;
+import cn.iven.lianji.api.dto.home.HomeStatsResponseDTO;
+import cn.iven.lianji.api.dto.home.MemoryTimelineItemDTO;
+import cn.iven.lianji.application.HomeStatsResult;
+import org.springframework.stereotype.Component;
+
+import java.util.List;
+
+/**
+ * 首页响应转换器。
+ * <p>负责 {@code HomeStatsResult → HomeStatsResponseDTO} 的出站转换。</p>
+ */
+@Component
+public class HomeResponseConverter {
+
+    public HomeStatsResponseDTO toDTO(HomeStatsResult result) {
+        if (result == null) {
+            return null;
+        }
+        return HomeStatsResponseDTO.builder()
+                .daysTogether(result.daysTogether())
+                .memoryCount(result.memoryCount())
+                .locationCount(result.locationCount())
+                .messageCount(result.messageCount())
+                .achievementCount(result.achievementCount())
+                .upcomingAnniversaries(toAnniversaryCardDTOList(result.upcomingAnniversaries()))
+                .recentMemories(toMemoryTimelineItemDTOList(result.recentMemories()))
+                .build();
+    }
+
+    private List<AnniversaryCardDTO> toAnniversaryCardDTOList(
+            List<HomeStatsResult.AnniversaryCardResult> list) {
+        if (list == null) {
+            return null;
+        }
+        return list.stream()
+                .map(this::toAnniversaryCardDTO)
+                .toList();
+    }
+
+    private AnniversaryCardDTO toAnniversaryCardDTO(HomeStatsResult.AnniversaryCardResult item) {
+        if (item == null) {
+            return null;
+        }
+        return AnniversaryCardDTO.builder()
+                .title(item.title())
+                .remainingDays(item.remainingDays())
+                .build();
+    }
+
+    private List<MemoryTimelineItemDTO> toMemoryTimelineItemDTOList(
+            List<HomeStatsResult.MemoryTimelineItemResult> list) {
+        if (list == null) {
+            return null;
+        }
+        return list.stream()
+                .map(this::toMemoryTimelineItemDTO)
+                .toList();
+    }
+
+    private MemoryTimelineItemDTO toMemoryTimelineItemDTO(HomeStatsResult.MemoryTimelineItemResult item) {
+        if (item == null) {
+            return null;
+        }
+        return MemoryTimelineItemDTO.builder()
+                .id(item.id())
+                .title(item.title())
+                .description(item.description())
+                .date(item.date())
+                .mood(item.mood())
+                .build();
+    }
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/home/AnniversaryCardDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/home/AnniversaryCardDTO.java
new file mode 100644
index 0000000..73d835d
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/home/AnniversaryCardDTO.java
@@ -0,0 +1,18 @@
+package cn.iven.lianji.api.dto.home;
+
+import lombok.Builder;
+import lombok.Data;
+
+/**
+ * 纪念日卡片 DTO。
+ */
+@Data
+@Builder
+public class AnniversaryCardDTO {
+
+    /** 纪念日标题 */
+    private String title;
+
+    /** 距离纪念日的剩余天数 */
+    private Integer remainingDays;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/home/HomeStatsResponseDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/home/HomeStatsResponseDTO.java
new file mode 100644
index 0000000..d14cedb
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/home/HomeStatsResponseDTO.java
@@ -0,0 +1,36 @@
+package cn.iven.lianji.api.dto.home;
+
+import lombok.Builder;
+import lombok.Data;
+
+import java.util.List;
+
+/**
+ * 首页统计数据响应 DTO。
+ * <p>包含情侣在一起天数、各类统计数量、即将到来的纪念日及最近回忆。</p>
+ */
+@Data
+@Builder
+public class HomeStatsResponseDTO {
+
+    /** 在一起天数 */
+    private Integer daysTogether;
+
+    /** 回忆总数 */
+    private Integer memoryCount;
+
+    /** 地点打卡数 */
+    private Integer locationCount;
+
+    /** 消息数 */
+    private Integer messageCount;
+
+    /** 成就数 */
+    private Integer achievementCount;
+
+    /** 即将到来的纪念日列表 */
+    private List<AnniversaryCardDTO> upcomingAnniversaries;
+
+    /** 最近回忆时间线 */
+    private List<MemoryTimelineItemDTO> recentMemories;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/home/MemoryTimelineItemDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/home/MemoryTimelineItemDTO.java
new file mode 100644
index 0000000..a66ccb3
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/home/MemoryTimelineItemDTO.java
@@ -0,0 +1,27 @@
+package cn.iven.lianji.api.dto.home;
+
+import lombok.Builder;
+import lombok.Data;
+
+/**
+ * 回忆时间线条目 DTO。
+ */
+@Data
+@Builder
+public class MemoryTimelineItemDTO {
+
+    /** 回忆 ID */
+    private Long id;
+
+    /** 回忆标题 */
+    private String title;
+
+    /** 回忆描述 */
+    private String description;
+
+    /** 回忆日期（yyyy-MM-dd） */
+    private String date;
+
+    /** 心情指数（1-5） */
+    private Integer mood;
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/HomeStatsResult.java b/src/api/src/main/java/cn/iven/lianji/application/HomeStatsResult.java
new file mode 100644
index 0000000..ab5853b
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/HomeStatsResult.java
@@ -0,0 +1,21 @@
+package cn.iven.lianji.application;
+
+import java.util.List;
+
+/**
+ * 首页统计数据应用层结果对象。
+ * <p>封装首页展示所需的统计数据，供 API 层转换为 {@code HomeStatsResponseDTO}。</p>
+ */
+public record HomeStatsResult(
+        Integer daysTogether,
+        Integer memoryCount,
+        Integer locationCount,
+        Integer messageCount,
+        Integer achievementCount,
+        List<AnniversaryCardResult> upcomingAnniversaries,
+        List<MemoryTimelineItemResult> recentMemories
+) {
+    public record AnniversaryCardResult(String title, Integer remainingDays) {}
+
+    public record MemoryTimelineItemResult(Long id, String title, String description, String date, Integer mood) {}
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/HomeAppService.java b/src/api/src/main/java/cn/iven/lianji/application/service/HomeAppService.java
new file mode 100644
index 0000000..b00f8f5
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/HomeAppService.java
@@ -0,0 +1,18 @@
+package cn.iven.lianji.application.service;
+
+import cn.iven.lianji.application.HomeStatsResult;
+
+/**
+ * 首页应用服务接口。
+ * <p>编排首页统计数据查询用例。</p>
+ */
+public interface HomeAppService {
+
+    /**
+     * 获取首页统计数据。
+     *
+     * @param userId 当前用户 ID
+     * @return 首页统计数据
+     */
+    HomeStatsResult getStats(Long userId);
+}
diff --git a/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java b/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java
new file mode 100644
index 0000000..5b79fb8
--- /dev/null
+++ b/src/api/src/main/java/cn/iven/lianji/application/service/impl/HomeAppServiceImpl.java
@@ -0,0 +1,56 @@
+package cn.iven.lianji.application.service.impl;
+
+import cn.iven.lianji.application.HomeStatsResult;
+import cn.iven.lianji.application.service.HomeAppService;
+import cn.iven.lianji.domain.exception.ErrorCode;
+import cn.iven.lianji.domain.exception.ForbiddenException;
+import cn.iven.lianji.domain.model.entity.Couple;
+import cn.iven.lianji.domain.repository.CoupleRepository;
+import lombok.RequiredArgsConstructor;
+import org.springframework.stereotype.Service;
+
+import java.time.LocalDate;
+import java.time.temporal.ChronoUnit;
+import java.util.List;
+
+/**
+ * 首页应用服务实现。
+ */
+@Service
+@RequiredArgsConstructor
+public class HomeAppServiceImpl implements HomeAppService {
+
+    private final CoupleRepository coupleRepository;
+
+    @Override
+    public HomeStatsResult getStats(Long userId) {
+        Couple couple = coupleRepository.findByUserId(userId)
+                .orElseThrow(() -> new ForbiddenException(ErrorCode.Forbidden.FORBIDDEN, "用户未绑定情侣关系"));
+
+        int daysTogether = (int) ChronoUnit.DAYS.between(
+                couple.getCreatedAt().toLocalDate(), LocalDate.now());
+
+        List<HomeStatsResult.AnniversaryCardResult> upcomingAnniversaries = List.of(
+                new HomeStatsResult.AnniversaryCardResult("一周年纪念日", 3)
+        );
+
+        List<HomeStatsResult.MemoryTimelineItemResult> recentMemories = List.of(
+                new HomeStatsResult.MemoryTimelineItemResult(
+                        1L, "第一次约会", "今天和TA去了人民公园，天气很好...", "2026-05-18", 1),
+                new HomeStatsResult.MemoryTimelineItemResult(
+                        2L, "一起看电影", "看了《恋恋笔记本》，非常感动...", "2026-05-15", 2),
+                new HomeStatsResult.MemoryTimelineItemResult(
+                        3L, "一起做晚饭", "做了意大利面，虽然卖相不好但很好吃...", "2026-05-12", 3)
+        );
+
+        return new HomeStatsResult(
+                daysTogether,
+                52,
+                18,
+                128,
+                12,
+                upcomingAnniversaries,
+                recentMemories
+        );
+    }
+}
diff --git a/src/api/src/test/java/cn/iven/lianji/application/service/impl/HomeAppServiceImplTest.java b/src/api/src/test/java/cn/iven/lianji/application/service/impl/HomeAppServiceImplTest.java
new file mode 100644
index 0000000..9ed3f78
--- /dev/null
+++ b/src/api/src/test/java/cn/iven/lianji/application/service/impl/HomeAppServiceImplTest.java
@@ -0,0 +1,92 @@
+package cn.iven.lianji.application.service.impl;
+
+import cn.iven.lianji.application.HomeStatsResult;
+import cn.iven.lianji.domain.exception.ForbiddenException;
+import cn.iven.lianji.domain.model.entity.Couple;
+import cn.iven.lianji.domain.repository.CoupleRepository;
+import org.junit.jupiter.api.Test;
+import org.junit.jupiter.api.extension.ExtendWith;
+import org.mockito.InjectMocks;
+import org.mockito.Mock;
+import org.mockito.junit.jupiter.MockitoExtension;
+
+import java.time.LocalDate;
+import java.time.OffsetDateTime;
+import java.time.ZoneOffset;
+import java.time.temporal.ChronoUnit;
+import java.util.Optional;
+
+import static org.assertj.core.api.Assertions.assertThat;
+import static org.assertj.core.api.Assertions.assertThatThrownBy;
+import static org.mockito.Mockito.when;
+
+@ExtendWith(MockitoExtension.class)
+class HomeAppServiceImplTest {
+
+    @Mock
+    private CoupleRepository coupleRepository;
+
+    @InjectMocks
+    private HomeAppServiceImpl homeAppService;
+
+    @Test
+    void getStats_shouldReturnCorrectResultWhenCoupleExists() {
+        OffsetDateTime createdAt = OffsetDateTime.of(2024, 1, 1, 0, 0, 0, 0, ZoneOffset.UTC);
+        Couple couple = Couple.builder()
+                .id(1L)
+                .userAId(1L)
+                .userBId(2L)
+                .createdAt(createdAt)
+                .build();
+        when(coupleRepository.findByUserId(1L)).thenReturn(Optional.of(couple));
+
+        HomeStatsResult result = homeAppService.getStats(1L);
+
+        int expectedDays = (int) ChronoUnit.DAYS.between(createdAt.toLocalDate(), LocalDate.now());
+
+        assertThat(result).isNotNull();
+        assertThat(result.daysTogether()).isEqualTo(expectedDays);
+        assertThat(result.memoryCount()).isEqualTo(52);
+        assertThat(result.locationCount()).isEqualTo(18);
+        assertThat(result.messageCount()).isEqualTo(128);
+        assertThat(result.achievementCount()).isEqualTo(12);
+
+        assertThat(result.upcomingAnniversaries()).hasSize(1);
+        assertThat(result.upcomingAnniversaries().get(0).title()).isEqualTo("一周年纪念日");
+        assertThat(result.upcomingAnniversaries().get(0).remainingDays()).isEqualTo(3);
+
+        assertThat(result.recentMemories()).hasSize(3);
+        assertThat(result.recentMemories().get(0).title()).isEqualTo("第一次约会");
+        assertThat(result.recentMemories().get(0).mood()).isEqualTo(1);
+        assertThat(result.recentMemories().get(1).mood()).isEqualTo(2);
+        assertThat(result.recentMemories().get(2).mood()).isEqualTo(3);
+    }
+
+    @Test
+    void getStats_shouldThrowForbiddenExceptionWhenNoCouple() {
+        when(coupleRepository.findByUserId(99L)).thenReturn(Optional.empty());
+
+        assertThatThrownBy(() -> homeAppService.getStats(99L))
+                .isInstanceOf(ForbiddenException.class)
+                .hasMessageContaining("用户未绑定情侣关系");
+    }
+
+    @Test
+    void getStats_shouldCalculateDaysTogetherCorrectly() {
+        OffsetDateTime createdAt = OffsetDateTime.of(2026, 5, 10, 12, 0, 0, 0, ZoneOffset.UTC);
+        Couple couple = Couple.builder()
+                .id(1L)
+                .userAId(1L)
+                .userBId(2L)
+                .createdAt(createdAt)
+                .build();
+        when(coupleRepository.findByUserId(1L)).thenReturn(Optional.of(couple));
+
+        HomeStatsResult result = homeAppService.getStats(1L);
+
+        int expectedDays = (int) ChronoUnit.DAYS.between(
+                createdAt.toLocalDate(), LocalDate.now());
+        assertThat(result.daysTogether()).isEqualTo(expectedDays);
+        assertThat(result.daysTogether()).isEqualTo(6);
+    }
+}
```

### `c640ffa8` fix(backend): 修复 TIMESTAMPTZ 类型不匹配并移除审计字段

- **时间:** 2026-05-16 00:48:32 +0800

**提交信息:**

fix(backend): 修复 TIMESTAMPTZ 类型不匹配并移除审计字段

- 将 Couple 相关类的 createdAt 从 LocalDateTime 改为 OffsetDateTime
  以匹配 PostgreSQL TIMESTAMPTZ 类型
- 移除 UserDO 的 createdAt/updatedAt 审计字段
- 新增 Flyway 迁移 V1.1__remove_audit_fields.sql

**代码变更:**

```diff
diff --git a/src/api/src/main/java/cn/iven/lianji/api/dto/couple/CoupleResponseDTO.java b/src/api/src/main/java/cn/iven/lianji/api/dto/couple/CoupleResponseDTO.java
index f477fe2..5cacd75 100644
--- a/src/api/src/main/java/cn/iven/lianji/api/dto/couple/CoupleResponseDTO.java
+++ b/src/api/src/main/java/cn/iven/lianji/api/dto/couple/CoupleResponseDTO.java
@@ -3,7 +3,7 @@ package cn.iven.lianji.api.dto.couple;
 import lombok.Builder;
 import lombok.Data;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 /**
  * 情侣关系响应 DTO。
@@ -22,5 +22,5 @@ public class CoupleResponseDTO {
     private Long userBId;
 
     /** 关系建立时间 */
-    private LocalDateTime createdAt;
+    private OffsetDateTime createdAt;
 }
diff --git a/src/api/src/main/java/cn/iven/lianji/application/CoupleResult.java b/src/api/src/main/java/cn/iven/lianji/application/CoupleResult.java
index a779e0e..c29ef6c 100644
--- a/src/api/src/main/java/cn/iven/lianji/application/CoupleResult.java
+++ b/src/api/src/main/java/cn/iven/lianji/application/CoupleResult.java
@@ -1,6 +1,6 @@
 package cn.iven.lianji.application;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 /**
  * 情侣关系应用层结果对象。
@@ -10,5 +10,5 @@ public record CoupleResult(
         Long id,
         Long userAId,
         Long userBId,
-        LocalDateTime createdAt
+        OffsetDateTime createdAt
 ) {}
diff --git a/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
index dc59d46..2469e41 100644
--- a/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
+++ b/src/api/src/main/java/cn/iven/lianji/domain/model/entity/Couple.java
@@ -3,7 +3,7 @@ package cn.iven.lianji.domain.model.entity;
 import lombok.Builder;
 import lombok.Data;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 /**
  * 情侣关系领域实体。
@@ -16,7 +16,7 @@ public class Couple {
     private Long id;
     private Long userAId;
     private Long userBId;
-    private LocalDateTime createdAt;
+    private OffsetDateTime createdAt;
 
     /**
      * 工厂方法：创建新的情侣关系。
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/CoupleDO.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/CoupleDO.java
index 69399e2..f17692e 100644
--- a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/CoupleDO.java
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/CoupleDO.java
@@ -6,7 +6,7 @@ import com.baomidou.mybatisplus.annotation.TableName;
 import lombok.Builder;
 import lombok.Data;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 /**
  * 情侣关系数据持久化对象（DO）。
@@ -28,5 +28,5 @@ public class CoupleDO {
     private Long userBId;
 
     /** 关系建立时间 */
-    private LocalDateTime createdAt;
+    private OffsetDateTime createdAt;
 }
diff --git a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/UserDO.java b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/UserDO.java
index 47f8dd4..94bbc6b 100644
--- a/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/UserDO.java
+++ b/src/api/src/main/java/cn/iven/lianji/infrastructure/repository/dataobject/UserDO.java
@@ -6,8 +6,6 @@ import com.baomidou.mybatisplus.annotation.TableName;
 import lombok.Builder;
 import lombok.Data;
 
-import java.time.LocalDateTime;
-
 /**
  * 用户数据持久化对象（DO）。
  * <p>映射数据库表 {@code app_user}，供 MyBatis-Plus 使用。</p>
@@ -32,10 +30,4 @@ public class UserDO {
 
     /** 头像图片URL */
     private String avatarUrl;
-
-    /** 记录创建时间 */
-    private LocalDateTime createdAt;
-
-    /** 记录最后更新时间 */
-    private LocalDateTime updatedAt;
 }
diff --git a/src/api/src/main/resources/db/migration/V1.1__remove_audit_fields.sql b/src/api/src/main/resources/db/migration/V1.1__remove_audit_fields.sql
new file mode 100644
index 0000000..8d08914
--- /dev/null
+++ b/src/api/src/main/resources/db/migration/V1.1__remove_audit_fields.sql
@@ -0,0 +1,6 @@
+-- 删除审计字段 created_at / updated_at
+-- app_user 表（created_at / updated_at 为纯审计字段，移除）
+ALTER TABLE app_user DROP COLUMN IF EXISTS created_at;
+ALTER TABLE app_user DROP COLUMN IF EXISTS updated_at;
+
+-- couple_relationship 表保留 created_at（关系建立时间为业务数据，非审计字段）
diff --git a/src/api/src/test/java/cn/iven/lianji/api/controller/v1/couple/CoupleControllerTest.java b/src/api/src/test/java/cn/iven/lianji/api/controller/v1/couple/CoupleControllerTest.java
index 83d6167..ea94513 100644
--- a/src/api/src/test/java/cn/iven/lianji/api/controller/v1/couple/CoupleControllerTest.java
+++ b/src/api/src/test/java/cn/iven/lianji/api/controller/v1/couple/CoupleControllerTest.java
@@ -17,7 +17,7 @@ import org.springframework.security.test.context.support.WithMockUser;
 import org.springframework.test.context.bean.override.mockito.MockitoBean;
 import org.springframework.test.web.servlet.MockMvc;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 import static org.mockito.ArgumentMatchers.eq;
 import static org.mockito.Mockito.when;
@@ -65,10 +65,10 @@ class CoupleControllerTest {
     @Test
     @WithMockUser(username = "2")
     void bind_shouldReturn200AndCoupleResponse() throws Exception {
-        CoupleResult result = new CoupleResult(10L, 1L, 2L, LocalDateTime.of(2024, 1, 1, 0, 0));
+        CoupleResult result = new CoupleResult(10L, 1L, 2L, OffsetDateTime.of(2024, 1, 1, 0, 0, 0, 0, java.time.ZoneOffset.UTC));
         CoupleResponseDTO dto = CoupleResponseDTO.builder()
                 .id(10L).userAId(1L).userBId(2L)
-                .createdAt(LocalDateTime.of(2024, 1, 1, 0, 0))
+                .createdAt(OffsetDateTime.of(2024, 1, 1, 0, 0, 0, 0, java.time.ZoneOffset.UTC))
                 .build();
 
         when(coupleAppService.bind(eq(2L), eq("654321"))).thenReturn(result);
@@ -89,10 +89,10 @@ class CoupleControllerTest {
     @Test
     @WithMockUser(username = "5")
     void getStatus_shouldReturn200AndCoupleResponse() throws Exception {
-        CoupleResult result = new CoupleResult(20L, 5L, 6L, LocalDateTime.of(2024, 6, 1, 10, 0));
+        CoupleResult result = new CoupleResult(20L, 5L, 6L, OffsetDateTime.of(2024, 6, 1, 10, 0, 0, 0, java.time.ZoneOffset.UTC));
         CoupleResponseDTO dto = CoupleResponseDTO.builder()
                 .id(20L).userAId(5L).userBId(6L)
-                .createdAt(LocalDateTime.of(2024, 6, 1, 10, 0))
+                .createdAt(OffsetDateTime.of(2024, 6, 1, 10, 0, 0, 0, java.time.ZoneOffset.UTC))
                 .build();
 
         when(coupleAppService.getRelationship(5L)).thenReturn(result);
diff --git a/src/api/src/test/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImplTest.java b/src/api/src/test/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImplTest.java
index c6213b7..bac5ead 100644
--- a/src/api/src/test/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImplTest.java
+++ b/src/api/src/test/java/cn/iven/lianji/application/service/impl/CoupleAppServiceImplTest.java
@@ -15,7 +15,7 @@ import org.springframework.data.redis.core.StringRedisTemplate;
 import org.springframework.data.redis.core.ValueOperations;
 
 import java.time.Duration;
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 import java.util.Optional;
 
 import static org.assertj.core.api.Assertions.assertThat;
@@ -88,7 +88,7 @@ class CoupleAppServiceImplTest {
         when(coupleRepository.save(any(Couple.class))).thenAnswer(inv -> {
             Couple c = inv.getArgument(0);
             c.setId(100L);
-            c.setCreatedAt(LocalDateTime.of(2024, 1, 1, 0, 0));
+            c.setCreatedAt(OffsetDateTime.of(2024, 1, 1, 0, 0, 0, 0, java.time.ZoneOffset.UTC));
             return c;
         });
 
@@ -159,7 +159,7 @@ class CoupleAppServiceImplTest {
                 .id(50L)
                 .userAId(5L)
                 .userBId(6L)
-                .createdAt(LocalDateTime.of(2024, 6, 1, 10, 0))
+                .createdAt(OffsetDateTime.of(2024, 6, 1, 10, 0, 0, 0, java.time.ZoneOffset.UTC))
                 .build();
         when(coupleRepository.findByUserId(5L)).thenReturn(Optional.of(couple));
 
diff --git a/src/api/src/test/java/cn/iven/lianji/infrastructure/repository/converter/CoupleRepositoryConverterTest.java b/src/api/src/test/java/cn/iven/lianji/infrastructure/repository/converter/CoupleRepositoryConverterTest.java
index de1208a..b930be0 100644
--- a/src/api/src/test/java/cn/iven/lianji/infrastructure/repository/converter/CoupleRepositoryConverterTest.java
+++ b/src/api/src/test/java/cn/iven/lianji/infrastructure/repository/converter/CoupleRepositoryConverterTest.java
@@ -4,7 +4,7 @@ import cn.iven.lianji.domain.model.entity.Couple;
 import cn.iven.lianji.infrastructure.repository.dataobject.CoupleDO;
 import org.junit.jupiter.api.Test;
 
-import java.time.LocalDateTime;
+import java.time.OffsetDateTime;
 
 import static org.assertj.core.api.Assertions.assertThat;
 
@@ -14,7 +14,7 @@ class CoupleRepositoryConverterTest {
 
     @Test
     void toDataObject_shouldMapAllFields() {
-        LocalDateTime now = LocalDateTime.of(2024, 1, 1, 12, 0);
+        OffsetDateTime now = OffsetDateTime.of(2024, 1, 1, 12, 0, 0, 0, java.time.ZoneOffset.UTC);
         Couple entity = Couple.builder()
                 .id(1L)
                 .userAId(10L)
@@ -37,7 +37,7 @@ class CoupleRepositoryConverterTest {
 
     @Test
     void toEntity_shouldMapAllFields() {
-        LocalDateTime now = LocalDateTime.of(2024, 6, 15, 8, 30);
+        OffsetDateTime now = OffsetDateTime.of(2024, 6, 15, 8, 30, 0, 0, java.time.ZoneOffset.UTC);
         CoupleDO dataObject = CoupleDO.builder()
                 .id(2L)
                 .userAId(30L)
@@ -60,7 +60,7 @@ class CoupleRepositoryConverterTest {
 
     @Test
     void roundTrip_shouldPreserveData() {
-        LocalDateTime now = LocalDateTime.now();
+        OffsetDateTime now = OffsetDateTime.now(java.time.ZoneOffset.UTC);
         Couple original = Couple.builder()
                 .id(5L)
                 .userAId(100L)
```
