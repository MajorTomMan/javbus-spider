package com.javbus.spider.spider.controller.base;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;

import com.javbus.spider.spider.service.base.ImageService;
import com.javbus.spider.spider.utils.R;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

@Controller
@RequestMapping("image")
public class ImageController {
    @Autowired
    private ImageService imageService;

    @GetMapping("query/{code}")
    public String queryImage(@PathVariable String code, Model model) {
        if (code == null) {
            return null;
        }
        List<byte[]> images=new ArrayList<>();
        try {
            images = imageService.getImagesByCode(code);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
         
        // 将每个字节数组转换为Base64字符串，并添加到列表中
        List<String> base64Images = new ArrayList<>();
        for (byte[] bytes : images) {
            String base64Image = Base64.getEncoder().encodeToString(bytes);
            base64Images.add(base64Image);
        }

        // 将Base64字符串列表传递给Thymeleaf模板
        model.addAttribute("base64Images", base64Images);
        return "images";
    }

    @GetMapping("query/{isCensored}/{pageSize}/{offset}")
    @ResponseBody
    public R queryAllMovieCode(@PathVariable Boolean isCensored, @PathVariable Integer pageSize,
            @PathVariable Integer offset) {
        if (isCensored == null || pageSize == null || offset == null || offset < 0 || pageSize < 0) {
            return R.error();
        }
        List<String> codes = imageService.queryAllMovieCode(isCensored, pageSize, offset);
        return R.ok().put("code", codes);
    }

}
