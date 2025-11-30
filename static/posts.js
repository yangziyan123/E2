document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("post-list");

    // 确认 JS 是否加载成功
    console.log("posts.js loaded");

    fetch("/api/posts")
        .then(res => {
            console.log("API 状态码:", res.status);
            return res.json();
        })
        .then(posts => {
            console.log("API 数据:", posts);

            container.innerHTML = "";

            if (!posts || posts.length === 0) {
                container.innerHTML = "<p>暂无文章。</p>";
                return;
            }

            posts.forEach(post => {
                const card = document.createElement("div");
                card.className = "post-card";

                card.innerHTML = `
                    <div class="post-title">${post.title}</div>

                    <div class="post-meta">
                        <span class="post-status">${post.status}</span>
                    </div>

                    <div class="post-excerpt">
                        ${post.content ? post.content.slice(0, 10) + "..." : ""}
                    </div>
                `;

                // 点击跳转文章详情（你以后可以换成动态模板）
                card.addEventListener("click", () => {
                    window.location.href = "/static/post.html?id=" + post.id;
                });

                container.appendChild(card);
            });
        })
        .catch(err => {
            console.error("加载失败:", err);
            container.innerHTML = "<p>加载失败，请检查 API 是否可用。</p>";
        });
});
