 using UnityEngine;

public class Block : MonoBehaviour
{
    private SpriteRenderer spriteRenderer;
    
    // 方块颜色定义
    public static readonly Color[] COLORS = new Color[]
    {
        new Color(0f, 1f, 1f),      // I - 青色
        new Color(1f, 1f, 0f),      // O - 黄色
        new Color(0.5f, 0f, 0.5f),  // T - 紫色
        new Color(1f, 0.65f, 0f),   // L - 橙色
        new Color(0f, 0f, 1f),      // J - 蓝色
        new Color(0f, 1f, 0f),      // S - 绿色
        new Color(1f, 0f, 0f)       // Z - 红色
    };

    private void Awake()
    {
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    public void SetColor(int colorIndex)
    {
        if (colorIndex >= 0 && colorIndex < COLORS.Length)
        {
            spriteRenderer.color = COLORS[colorIndex];
        }
    }
}